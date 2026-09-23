from django.conf import settings
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone

from .models import Answer, Category, TestAttempt


def test_list(request):
    categories = Category.objects.all()
    profile = request.user.profile if request.user.is_authenticated else None
    return render(
        request,
        "iqtest/test_list.html",
        {"categories": categories, "profile": profile},
    )


def _score_to_iq(percentage: int) -> int:
    """
    Very simplified mapping from a raw percentage score to an IQ-style
    number, centered on 100. This is NOT a validated psychometric
    instrument -- it's a stand-in you can replace with real norming data.
    """
    return round(70 + (percentage / 100) * 60)


@login_required
def take_test(request, slug):
    category = get_object_or_404(Category, slug=slug)
    profile = request.user.profile

    if category.is_premium and not profile.has_premium_access:
        messages.info(request, "That category is part of Premium. Upgrade to unlock it.")
        return redirect("billing:pricing")

    questions = category.questions.prefetch_related("choices").all()

    if request.method == "POST":
        if not questions:
            messages.error(request, "This category has no questions yet.")
            return redirect("iqtest:test_list")

        within_free_quota = profile.free_test_attempts_used < settings.FREE_TEST_ATTEMPTS_LIMIT
        detail_unlocked = profile.has_premium_access or within_free_quota

        attempt = TestAttempt.objects.create(
            user=request.user,
            category=category,
            total_questions=questions.count(),
            detail_unlocked=detail_unlocked,
        )

        score = 0
        answers = []
        for question in questions:
            choice_id = request.POST.get(f"question_{question.id}")
            choice = None
            is_correct = False
            if choice_id:
                choice = question.choices.filter(id=choice_id).first()
                is_correct = bool(choice and choice.is_correct)
            if is_correct:
                score += 1
            answers.append(Answer(attempt=attempt, question=question, choice=choice, is_correct=is_correct))
        Answer.objects.bulk_create(answers)

        attempt.score = score
        attempt.completed_at = timezone.now()
        attempt.iq_score = _score_to_iq(attempt.percentage) if detail_unlocked else None
        attempt.save()

        if not profile.has_premium_access and not category.is_premium and within_free_quota:
            profile.free_test_attempts_used += 1
            profile.save(update_fields=["free_test_attempts_used"])

        return redirect("iqtest:result_detail", pk=attempt.pk)

    return render(request, "iqtest/take_test.html", {"category": category, "questions": questions})


@login_required
def result_detail(request, pk):
    attempt = get_object_or_404(
        TestAttempt.objects.select_related("category"), pk=pk, user=request.user
    )
    answers = attempt.answers.select_related("question", "choice") if attempt.detail_unlocked else []
    return render(
        request,
        "iqtest/result.html",
        {"attempt": attempt, "answers": answers},
    )
