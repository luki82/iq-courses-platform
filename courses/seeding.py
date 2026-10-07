"""
Shared helper for course seed commands.

A course is described as plain data:

    COURSE = {"slug": ..., "title": ..., "description": ...}
    MODULES = [
        # (module title, is_free_preview, [(lesson slug, lesson title, content), ...])
        ("Module 1: ...", True, [("slug", "Title", '''lesson text'''), ...]),
    ]

seed_course() creates or updates everything to match, so seed commands are
safe to run on every deploy. Edit lesson text in the seed file (not in
admin) -- the next deploy will overwrite admin edits to seeded lessons.
"""
from textwrap import dedent

from django.db import transaction

from .models import Course, Lesson, Module


@transaction.atomic
def seed_course(course_data: dict, modules: list) -> tuple[Course, bool, int]:
    course, created = Course.objects.update_or_create(
        slug=course_data["slug"],
        defaults={
            "title": course_data["title"],
            "description": course_data["description"],
            "is_published": True,
        },
    )

    lesson_total = 0
    for m_order, (module_title, is_free, lessons) in enumerate(modules, start=1):
        module, _ = Module.objects.update_or_create(
            course=course,
            order=m_order,
            defaults={"title": module_title, "is_free_preview": is_free},
        )
        for l_order, (slug, title, content) in enumerate(lessons, start=1):
            Lesson.objects.update_or_create(
                module=module,
                slug=slug,
                defaults={"title": title, "content": dedent(content).strip(), "order": l_order},
            )
            lesson_total += 1

    return course, created, lesson_total
