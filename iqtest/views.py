import logging
import time

import stripe
from django.conf import settings
from django.contrib import messages
from django.contrib.auth.views import redirect_to_login
from django.http import Http404
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone
from django.views.decorators.http import require_POST

from . import payments
from .models import Answer, Category, TestAttempt, TestPass

logger = logging.getLogger(__name__)

# The headline test shown first on the test list and on the home page.
FEATURED_SLUG = "full-iq-assessment"

# Answers submitted more than this long after a timed test's time limit are
# ignored. Covers slow connections and the auto-submit round trip.
LATE_GRACE_SECONDS = 60

# Attempt IDs a visitor has taken in this browser, so guests (no account)
# can see their own results.
ATTEMPTS_SESSION_KEY = "iqtest_attempt_ids"


def test_list(request):
    categories = list(Category.objects.all())
    featured = [c for c in categories if c.slug == FEATURED_SLUG]
    practice_tests = [c for c in categories if c.slug != FEATURED_SLUG]
    return render(
        request,
        "iqtest/test_list.html",
        {"featured_tests": featured, "practice_tests": practice_tests},
    )


def _score_to_iq(percentage: int) -> int:
    """
    Very simplified mapping from a raw percentage score to an IQ-style
    number, centered on 100. This is NOT a validated psychometric
    instrument -- it's a stand-in you can replace with real norming data.
    """
    return round(70 + (percentage / 100) * 60)


# --- Old paid-test links ---------------------------------------------------
# Every test is free now. These views stay so that links and buttons from
# before the change (and private links people bought) keep working.

@require_POST
def buy_pass(request, slug):
    category = get_object_or_404(Category, slug=slug)
    return redirect("iqtest:take_test", slug=category.slug)


def pass_success(request):
    """
    Where Stripe used to send test buyers. Kept so anyone who paid just
    before tests went free still gets their pass recorded.
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
    if test_pass is not None:
        payments.remember_pass(request, test_pass)
        return redirect("iqtest:pass_detail", token=test_pass.token)
    return redirect("iqtest:test_list")


def pass_detail(request, token):
    """
    A private link from when the test was paid. It still brings the holder
    back to their result, or to the (now free) test.
    """
    test_pass = get_object_or_404(TestPass.objects.select_related("category"), token=token)
    payments.remember_pass(request, test_pass)
    if test_pass.is_used:
        return redirect("iqtest:result_detail", pk=test_pass.attempt_id)
    return redirect("iqtest:take_test", slug=test_pass.category.slug)


# --- Taking a test ---------------------------------------------------------

def _start_key(category) -> str:
    return f"iqtest_started_{category.id}"


# Untimed tests still record how long the attempt took; a start time older
# than this is treated as abandoned and the clock restarts on the next visit.
UNTIMED_STALE_SECONDS = 3 * 60 * 60


def _get_or_start_clock(request, category) -> float:
    """
    Remember when the visitor opened the test, in their session, so
    refreshing the page does not reset the countdown. A start time from an
    attempt that has already run out (or been abandoned) is replaced with a
    fresh one.
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


def _remember_attempt(request, attempt) -> None:
    ids = list(request.session.get(ATTEMPTS_SESSION_KEY, []))
    if attempt.pk not in ids:
        ids.append(attempt.pk)
        request.session[ATTEMPTS_SESSION_KEY] = ids


def take_test(request, slug):
    """Every test is free and open to everyone, with or without an account."""
    category = get_object_or_404(Category, slug=slug)
    questions = category.questions.prefetch_related("choices").all()
    if not questions:
        messages.error(request, "This test has no questions yet.")
        return redirect("iqtest:test_list")

    limit_seconds = (category.time_limit_minutes or 0) * 60

    if request.method == "POST":
        started = request.session.pop(_start_key(category), None)
        elapsed = time.time() - started if started else None
        too_late = bool(limit_seconds and elapsed) and elapsed > limit_seconds + LATE_GRACE_SECONDS
        if elapsed is not None and limit_seconds:
            elapsed = min(elapsed, limit_seconds)

        attempt = TestAttempt.objects.create(
            user=request.user if request.user.is_authenticated else None,
            category=category,
            total_questions=len(questions),
            detail_unlocked=True,
            time_taken_seconds=round(elapsed) if elapsed is not None else None,
        )
        attempt.score = _score_answers(request, attempt, questions, ignore_answers=too_late)
        attempt.completed_at = timezone.now()
        attempt.iq_score = _score_to_iq(attempt.percentage)
        attempt.save()
        _remember_attempt(request, attempt)

        if too_late:
            messages.warning(request, "Your answers arrived after the time limit, so they couldn't be counted.")
        return redirect("iqtest:result_detail", pk=attempt.pk)

    started = _get_or_start_clock(request, category)
    remaining_seconds = None
    if limit_seconds:
        remaining_seconds = max(0, round(limit_seconds - (time.time() - started)))

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
    owns_by_session = attempt.pk in request.session.get(ATTEMPTS_SESSION_KEY, [])
    owns_by_pass = test_pass is not None and test_pass.token in request.session.get(payments.SESSION_KEY, [])
    if not (owns_by_account or owns_by_session or owns_by_pass):
        if attempt.user_id and not request.user.is_authenticated:
            return redirect_to_login(request.get_full_path())
        raise Http404("No result found.")

    # Results that were locked behind Premium before everything went free.
    if not attempt.detail_unlocked:
        attempt.detail_unlocked = True
        attempt.iq_score = _score_to_iq(attempt.percentage)
        attempt.save(update_fields=["detail_unlocked", "iq_score"])

    answers = attempt.answers.select_related("question", "choice").prefetch_related("question__choices")
    private_link = (
        request.build_absolute_uri(test_pass.get_absolute_url()) if test_pass is not None else None
    )
    return render(
        request,
        "iqtest/result.html",
        {"attempt": attempt, "answers": answers, "private_link": private_link},
    )
