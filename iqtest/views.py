import logging
import time

import stripe
from django.conf import settings
from django.contrib import messages
from django.contrib.auth.views import redirect_to_login
from django.db import transaction
from django.http import Http404
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone
from django.views.decorators.http import require_POST

from . import payments
from .models import Answer, Category, TestAttempt, TestPass

logger = logging.getLogger(__name__)

# Answers submitted more than this long after a paid test's time limit are
# ignored. Covers slow connections and the auto-submit round trip.
LATE_GRACE_SECONDS = 60


def test_list(request):
    categories = Category.objects.all()
    paid_tests = [c for c in categories if c.is_paid_test]
    practice_tests = [c for c in categories if not c.is_paid_test]
    for category in paid_tests:
        category.ready_pass = payments.unused_pass_for(request, category)
    profile = request.user.profile if request.user.is_authenticated else None
    return render(
        request,
        "iqtest/test_list.html",
        {"paid_tests": paid_tests, "practice_tests": practice_tests, "profile": profile},
    )


def _score_to_iq(percentage: int) -> int:
    """
    Very simplified mapping from a raw percentage score to an IQ-style
    number, centered on 100. This is NOT a validated psychometric
    instrument -- it's a stand-in you can replace with real norming data.
    """
    return round(70 + (percentage / 100) * 60)


# --- Buying a test pass (no account needed) --------------------------------

@require_POST
def buy_pass(request, slug):
    category = get_object_or_404(Category, slug=slug)
    if not category.is_paid_test:
        return redirect("iqtest:take_test", slug=category.slug)

    existing = payments.unused_pass_for(request, category)
    if existing:
        messages.info(request, "You've already paid for this test -- you can start it now.")
        return redirect("iqtest:pass_detail", token=existing.token)

    try:
        checkout_url = payments.start_checkout(request, category)
    except payments.CheckoutUnavailable as exc:
        messages.error(request, str(exc))
        return redirect("iqtest:test_list")
    return redirect(checkout_url, permanent=False)


def pass_success(request):
    """
    Stripe sends the buyer here after paying. We confirm the payment with
    Stripe straight away, remember the pass in their session and show their
    private link. The webhook is the backstop if they close the tab early.
    """
    session_id = request.GET.get("session_id", "")
    test_pass = None
    if session_id and settings.STRIPE_SECRET_KEY:
        stripe.api_key = settings.STRIPE_SECRET_KEY
        try:
            session = stripe.checkout.Session.retrieve(session_id)
            test_pass = payments.fulfil_test_pass(session)
        except stripe.StripeError:
            logger.exception("Could not retrieve checkout session %s", session_id)

    if test_pass is None:
        # Not paid yet (rare: delayed payment methods) or an invalid link.
        if session_id:
            test_pass = TestPass.objects.filter(stripe_checkout_session_id=session_id).first()
        if test_pass is not None:
            payments.remember_pass(request, test_pass)
        return render(request, "iqtest/pass_pending.html", {"test_pass": test_pass}, status=200)

    payments.remember_pass(request, test_pass)
    return redirect("iqtest:pass_detail", token=test_pass.token)


def pass_detail(request, token):
    """
    The buyer's private link. Opening it on any device restores access: it
    shows the start screen if the test hasn't been taken, or the result.
    """
    test_pass = get_object_or_404(TestPass.objects.select_related("category"), token=token)
    if not test_pass.is_paid:
        return render(request, "iqtest/pass_pending.html", {"test_pass": test_pass})

    payments.remember_pass(request, test_pass)
    if test_pass.is_used:
        return redirect("iqtest:result_detail", pk=test_pass.attempt_id)

    category = test_pass.category
    private_link = request.build_absolute_uri()
    return render(
        request,
        "iqtest/pass_detail.html",
        {"test_pass": test_pass, "category": category, "private_link": private_link},
    )


# --- Taking a test ---------------------------------------------------------

def _start_key(category) -> str:
    return f"iqtest_started_{category.id}"


# Untimed tests still record how long the attempt took; a start time older
# than this is treated as abandoned and the clock restarts on the next visit.
UNTIMED_STALE_SECONDS = 3 * 60 * 60


def _get_or_start_clock(request, category) -> float:
    """
    For free/Premium tests: remember when the user opened the test, in their
    session, so refreshing the page does not reset the countdown. A start
    time from an attempt that has already run out (or been abandoned) is
    replaced with a fresh one.
    """
    key = _start_key(category)
    now = time.time()
    started = request.session.get(key)
    limit_seconds = (category.time_limit_minutes or 0) * 60
    stale_after = limit_seconds or UNTIMED_STALE_SECONDS
    if started is None or now - started >= stale_after:
        started = now
        request.session[key] = started
    return started


def _score_answers(request, attempt, questions, ignore_answers=False):
    score = 0
    answers = []
    for question in questions:
        choice_id = None if ignore_answers else request.POST.get(f"question_{question.id}")
        choice = None
        is_correct = False
        if choice_id:
            choice = next((c for c in question.choices.all() if str(c.id) == choice_id), None)
            is_correct = bool(choice and choice.is_correct)
        if is_correct:
            score += 1
        answers.append(Answer(attempt=attempt, question=question, choice=choice, is_correct=is_correct))
    Answer.objects.bulk_create(answers)
    return score


def take_test(request, slug):
    category = get_object_or_404(Category, slug=slug)
    if category.is_paid_test:
        return _take_paid_test(request, category)
    if not request.user.is_authenticated:
        return redirect_to_login(request.get_full_path())
    return _take_member_test(request, category)


def _take_paid_test(request, category):
    test_pass = payments.unused_pass_for(request, category)
    if test_pass is None:
        # Already used? Send them to their result rather than a dead end.
        used = payments.passes_in_session(request).filter(category=category, attempt__isnull=False).last()
        if used:
            return redirect("iqtest:result_detail", pk=used.attempt_id)
        messages.info(request, f"{category.name} is a one-off {category.price_display} test. Buy a pass to start.")
        return redirect("iqtest:test_list")

    questions = category.questions.prefetch_related("choices").all()
    if not questions:
        messages.error(request, "This test has no questions yet.")
        return redirect("iqtest:test_list")

    limit_seconds = (category.time_limit_minutes or 0) * 60

    if request.method == "POST":
        with transaction.atomic():
            test_pass = TestPass.objects.select_for_update().get(pk=test_pass.pk)
            if test_pass.is_used:
                # Double submit (e.g. button pressed while auto-submit fired).
                return redirect("iqtest:result_detail", pk=test_pass.attempt_id)

            now = timezone.now()
            started_at = test_pass.started_at or now
            elapsed = (now - started_at).total_seconds()
            too_late = bool(limit_seconds) and elapsed > limit_seconds + LATE_GRACE_SECONDS

            attempt = TestAttempt.objects.create(
                user=request.user if request.user.is_authenticated else None,
                category=category,
                total_questions=len(questions),
                detail_unlocked=True,
                time_taken_seconds=round(min(elapsed, limit_seconds) if limit_seconds else elapsed),
            )
            attempt.score = _score_answers(request, attempt, questions, ignore_answers=too_late)
            attempt.completed_at = now
            attempt.iq_score = _score_to_iq(attempt.percentage)
            attempt.save()

            test_pass.attempt = attempt
            test_pass.save(update_fields=["attempt"])

        if too_late:
            messages.warning(request, "Your answers arrived after the time limit, so they couldn't be counted.")
        return redirect("iqtest:result_detail", pk=attempt.pk)

    # GET: the clock starts the first time the test page is opened and is
    # stored on the pass, so it can't be reset by refreshing or changing device.
    if test_pass.started_at is None:
        TestPass.objects.filter(pk=test_pass.pk, started_at__isnull=True).update(started_at=timezone.now())
        test_pass.refresh_from_db(fields=["started_at"])

    remaining_seconds = None
    if limit_seconds:
        elapsed = (timezone.now() - test_pass.started_at).total_seconds()
        remaining_seconds = max(0, round(limit_seconds - elapsed))

    return render(
        request,
        "iqtest/take_test.html",
        {"category": category, "questions": questions, "remaining_seconds": remaining_seconds},
    )


def _take_member_test(request, category):
    profile = request.user.profile

    if category.is_premium and not profile.has_premium_access:
        messages.info(request, "That category is part of Premium. Upgrade to unlock it.")
        return redirect("billing:pricing")

    questions = category.questions.prefetch_related("choices").all()

    if request.method == "POST":
        if not questions:
            messages.error(request, "This category has no questions yet.")
            return redirect("iqtest:test_list")

        started = request.session.pop(_start_key(category), None)
        time_taken = round(time.time() - started) if started else None

        within_free_quota = profile.free_test_attempts_used < settings.FREE_TEST_ATTEMPTS_LIMIT
        detail_unlocked = profile.has_premium_access or within_free_quota

        attempt = TestAttempt.objects.create(
            user=request.user,
            category=category,
            total_questions=len(questions),
            detail_unlocked=detail_unlocked,
            time_taken_seconds=time_taken,
        )
        attempt.score = _score_answers(request, attempt, questions)
        attempt.completed_at = timezone.now()
        attempt.iq_score = _score_to_iq(attempt.percentage) if detail_unlocked else None
        attempt.save()

        if not profile.has_premium_access and not category.is_premium and within_free_quota:
            profile.free_test_attempts_used += 1
            profile.save(update_fields=["free_test_attempts_used"])

        return redirect("iqtest:result_detail", pk=attempt.pk)

    started = _get_or_start_clock(request, category)
    remaining_seconds = None
    if category.time_limit_minutes:
        elapsed = time.time() - started
        remaining_seconds = max(0, round(category.time_limit_minutes * 60 - elapsed))

    return render(
        request,
        "iqtest/take_test.html",
        {"category": category, "questions": questions, "remaining_seconds": remaining_seconds},
    )


# --- Results ---------------------------------------------------------------

def result_detail(request, pk):
    attempt = get_object_or_404(TestAttempt.objects.select_related("category"), pk=pk)

    test_pass = TestPass.objects.filter(attempt=attempt).first()
    owns_by_account = request.user.is_authenticated and attempt.user_id == request.user.id
    owns_by_pass = test_pass is not None and test_pass.token in request.session.get(payments.SESSION_KEY, [])
    if not (owns_by_account or owns_by_pass):
        if not request.user.is_authenticated and test_pass is None:
            return redirect_to_login(request.get_full_path())
        raise Http404("No result found.")

    answers = (
        attempt.answers.select_related("question", "choice").prefetch_related("question__choices")
        if attempt.detail_unlocked
        else []
    )
    private_link = (
        request.build_absolute_uri(test_pass.get_absolute_url()) if test_pass is not None else None
    )
    return render(
        request,
        "iqtest/result.html",
        {"attempt": attempt, "answers": answers, "test_pass": test_pass, "private_link": private_link},
    )
