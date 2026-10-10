from django.db.models import Count, Q
from django.shortcuts import render

from courses.models import Course
from iqtest.models import Category


def home(request):
    # The paid, timed IQ challenge (the Full IQ Assessment), if it's set up.
    challenge = Category.objects.filter(price_cents__isnull=False).exclude(price_cents=0).first()

    # A course is free when every one of its modules is a free preview.
    courses = list(
        Course.objects.filter(is_published=True)
        .annotate(
            module_total=Count("modules", distinct=True),
            paid_modules=Count("modules", filter=Q(modules__is_free_preview=False), distinct=True),
        )
        .order_by("created_at")[:6]
    )
    for course in courses:
        course.is_free = course.module_total > 0 and course.paid_modules == 0
    free_course = next((c for c in courses if c.is_free), None)

    return render(
        request,
        "core/home.html",
        {"challenge": challenge, "courses": courses, "free_course": free_course},
    )
