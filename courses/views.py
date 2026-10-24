from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone

from .lesson_format import parse_lesson
from .models import Course, Enrollment, Lesson, LessonProgress


def course_list(request):
    courses = Course.objects.filter(is_published=True)
    return render(request, "courses/course_list.html", {"courses": courses})


def course_detail(request, slug):
    course = get_object_or_404(Course, slug=slug, is_published=True)
    is_enrolled = (
        request.user.is_authenticated
        and Enrollment.objects.filter(user=request.user, course=course).exists()
    )
    modules = course.modules.prefetch_related("lessons")

    completed_lesson_ids = set()
    if request.user.is_authenticated:
        completed_lesson_ids = set(
            LessonProgress.objects.filter(
                user=request.user, lesson__module__course=course, completed=True
            ).values_list("lesson_id", flat=True)
        )

    return render(
        request,
        "courses/course_detail.html",
        {
            "course": course,
            "modules": modules,
            "is_enrolled": is_enrolled,
            "completed_lesson_ids": completed_lesson_ids,
        },
    )


@login_required
def enroll(request, course_slug):
    course = get_object_or_404(Course, slug=course_slug, is_published=True)
    Enrollment.objects.get_or_create(user=request.user, course=course)
    messages.success(request, f"You're enrolled in {course.title}.")
    return redirect("courses:course_detail", slug=course.slug)


def lesson_detail(request, course_slug, lesson_id):
    """Lessons are public so anyone (and Google) can read them; accounts just track progress."""
    course = get_object_or_404(Course, slug=course_slug, is_published=True)
    lesson = get_object_or_404(Lesson, id=lesson_id, module__course=course)

    progress = None
    if request.user.is_authenticated:
        progress = LessonProgress.objects.filter(user=request.user, lesson=lesson).first()

    return render(
        request,
        "courses/lesson_detail.html",
        {
            "course": course,
            "lesson": lesson,
            "progress": progress,
            "blocks": parse_lesson(lesson.content, seed=lesson.slug),
        },
    )


@login_required
def mark_complete(request, course_slug, lesson_id):
    course = get_object_or_404(Course, slug=course_slug, is_published=True)
    lesson = get_object_or_404(Lesson, id=lesson_id, module__course=course)

    Enrollment.objects.get_or_create(user=request.user, course=course)
    progress, _ = LessonProgress.objects.get_or_create(user=request.user, lesson=lesson)
    progress.completed = True
    progress.completed_at = timezone.now()
    progress.save()
    messages.success(request, f"Marked '{lesson.title}' as complete.")
    return redirect("courses:course_detail", slug=course.slug)
