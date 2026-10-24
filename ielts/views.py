from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, render

from .models import IELTSLesson


def lesson_list(request):
    lessons = IELTSLesson.objects.all()
    return render(request, "ielts/lesson_list.html", {"lessons": lessons})


@login_required
def lesson_detail(request, slug):
    lesson = get_object_or_404(IELTSLesson, slug=slug)
    return render(
        request,
        "ielts/lesson_detail.html",
        {"lesson": lesson, "questions": lesson.questions.all()},
    )
