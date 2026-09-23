from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone

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
    has_premium = request.user.is_authenticated and request.user.profile.has_premium_access
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
            "has_premium": has_premium,
            "completed_lesson_ids": completed_lesson_ids,
        },
    )


@login_required
def enroll(request, course_slug):
    course = get_object_or_404(Course, slug=course_slug, is_published=True)
    Enrollment.objects.get_or_create(user=request.user, course=course)
    messages.success(request, f"You're enrolled in {course.title}.")
    return redirect("courses:course_detail", slug=course.slug)


@login_required
def lesson_detail(request, course_slug, lesson_id):
    course = get_object_or_404(Course, slug=course_slug, is_published=True)
    lesson = get_object_or_404(Lesson, id=lesson_id, module__course=course)

    if not Enrollment.objects.filter(user=request.user, course=course).exists():
        messages.info(request, "Enroll in this course first.")
        return redirect("courses:course_detail", slug=course.slug)

    if not lesson.is_free and not request.user.profile.has_premium_access:
        messages.info(request, "This lesson is part of Premium. Upgrade to keep going.")
        return redirect("billing:pricing")

    progress, _ = LessonProgress.objects.get_or_create(user=request.user, lesson=lesson)

    return render(
        request,
        "courses/lesson_detail.html",
        {"course": course, "lesson": lesson, "progress": progress},
    )


@login_required
def mark_complete(request, course_slug, lesson_id):
    course = get_object_or_404(Course, slug=course_slug, is_published=True)
    lesson = get_object_or_404(Lesson, id=lesson_id, module__course=course)

    if not lesson.is_free and not request.user.profile.has_premium_access:
        return redirect("billing:pricing")

    progress, _ = LessonProgress.objects.get_or_create(user=request.user, lesson=lesson)
    progress.completed = True
    progress.completed_at = timezone.now()
    progress.save()
    messages.success(request, f"Marked '{lesson.title}' as complete.")
    return redirect("courses:course_detail", slug=course.slug)
