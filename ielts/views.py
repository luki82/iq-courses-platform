from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render

from .models import IELTSLesson


def lesson_list(request):
    lessons = IELTSLesson.objects.all()
    return render(request, "ielts/lesson_list.html", {"lessons": lessons})


@login_required
def lesson_detail(request, slug):
    lesson = get_object_or_404(IELTSLesson, slug=slug)
    profile = request.user.profile

    if lesson.requires_premium and not profile.has_premium_access:
        messages.info(request, "That lesson is part of Premium. Upgrade to unlock it.")
        return redirect("billing:pricing")

    return render(
        request,
        "ielts/lesson_detail.html",
        {"lesson": lesson, "questions": lesson.questions.all()},
    )
