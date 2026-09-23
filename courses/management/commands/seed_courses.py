from django.core.management.base import BaseCommand

from courses.models import Course, Lesson, Module


class Command(BaseCommand):
    help = "Creates a sample course with a free preview module and a premium module."

    def handle(self, *args, **options):
        course, _ = Course.objects.get_or_create(
            slug="brain-training-101",
            defaults={
                "title": "Brain Training 101",
                "description": "A beginner-friendly course on memory, logic and focus techniques.",
                "is_published": True,
            },
        )

        if not course.modules.exists():
            free_module = Module.objects.create(
                course=course, title="Getting Started", order=1, is_free_preview=True
            )
            Lesson.objects.create(
                module=free_module,
                title="Welcome & How This Course Works",
                content="Welcome! In this course you'll build practical memory and logic skills, "
                "one short lesson at a time.",
                order=1,
            )
            Lesson.objects.create(
                module=free_module,
                title="The Basics of Working Memory",
                content="Working memory is how many things you can hold in mind at once. "
                "Try the exercises in this lesson daily for a week.",
                order=2,
            )

            premium_module = Module.objects.create(
                course=course, title="Advanced Techniques", order=2, is_free_preview=False
            )
            Lesson.objects.create(
                module=premium_module,
                title="Memory Palaces",
                content="A deep dive into the method of loci, used by memory champions worldwide.",
                order=1,
            )
            Lesson.objects.create(
                module=premium_module,
                title="Speed Logic Drills",
                content="Timed drills to sharpen pattern recognition and deductive reasoning.",
                order=2,
            )

        self.stdout.write(self.style.SUCCESS("Course sample data seeded."))
