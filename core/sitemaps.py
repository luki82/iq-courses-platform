"""
sitemap.xml for Google Search Console: every public page worth indexing.
Submit https://lorrank.com/sitemap.xml in Search Console > Sitemaps.
"""
from django.contrib.sitemaps import Sitemap
from django.urls import reverse

from courses.models import Course, Lesson
from ielts.models import IELTSLesson


class HttpsSitemap(Sitemap):
    protocol = "https"


class StaticPagesSitemap(HttpsSitemap):
    priority = 0.8
    changefreq = "weekly"

    def items(self):
        return [
            "core:home",
            "iqtest:test_list",
            "courses:course_list",
            "ielts:lesson_list",
            "billing:donate",
            "core:about",
            "core:privacy",
            "core:contact",
        ]

    def location(self, item):
        return reverse(item)


class CourseSitemap(HttpsSitemap):
    priority = 0.7
    changefreq = "weekly"

    def items(self):
        return Course.objects.filter(is_published=True).order_by("id")

    def location(self, course):
        return reverse("courses:course_detail", args=[course.slug])


class LessonSitemap(HttpsSitemap):
    priority = 0.6
    changefreq = "monthly"

    def items(self):
        return (
            Lesson.objects.filter(module__course__is_published=True)
            .select_related("module__course")
            .order_by("id")
        )

    def location(self, lesson):
        return reverse("courses:lesson_detail", args=[lesson.module.course.slug, lesson.id])


class IELTSLessonSitemap(HttpsSitemap):
    priority = 0.6
    changefreq = "monthly"

    def items(self):
        return IELTSLesson.objects.order_by("id")

    def location(self, lesson):
        return reverse("ielts:lesson_detail", args=[lesson.slug])

    def lastmod(self, lesson):
        return lesson.created_at


sitemaps = {
    "pages": StaticPagesSitemap,
    "courses": CourseSitemap,
    "lessons": LessonSitemap,
    "ielts": IELTSLessonSitemap,
}
