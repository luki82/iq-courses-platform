from django.core.management import call_command
from django.test import TestCase, override_settings
from django.urls import reverse

from courses.models import Course, Lesson
from ielts.models import IELTSLesson

plain_static = override_settings(
    STORAGES={
        "default": {"BACKEND": "django.core.files.storage.FileSystemStorage"},
        "staticfiles": {"BACKEND": "django.contrib.staticfiles.storage.StaticFilesStorage"},
    }
)


@plain_static
class SearchReadinessTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        call_command("seed_english_esl", stdout=open("/dev/null", "w"))
        cls.course = Course.objects.get(slug="english-for-beginners")
        cls.lesson = Lesson.objects.filter(module__course=cls.course).first()
        cls.ielts = IELTSLesson.objects.create(
            module_title="Foundation", tier="TIER_1", skill="READING", title="Urban bees",
            passage_or_prompt="Bees are thriving in cities.",
        )

    def test_guest_can_read_course_lesson(self):
        response = self.client.get(reverse("courses:lesson_detail", args=[self.course.slug, self.lesson.id]))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Create a free account")
        self.assertContains(response, '<meta name="description"')

    def test_guest_sees_open_links_on_course_page(self):
        response = self.client.get(reverse("courses:course_detail", args=[self.course.slug]))
        self.assertContains(response, reverse("courses:lesson_detail", args=[self.course.slug, self.lesson.id]))
        self.assertNotContains(response, "Enroll to access")

    def test_guest_can_read_ielts_lesson(self):
        response = self.client.get(reverse("ielts:lesson_detail", args=[self.ielts.slug]))
        self.assertContains(response, "IELTS Reading: Urban bees")

    def test_sitemap_lists_lessons(self):
        xml = self.client.get("/sitemap.xml").content.decode()
        self.assertIn(reverse("courses:lesson_detail", args=[self.course.slug, self.lesson.id]), xml)
        self.assertIn(reverse("ielts:lesson_detail", args=[self.ielts.slug]), xml)
        self.assertIn(reverse("core:privacy"), xml)
        self.assertIn("https://", xml)

    def test_robots_points_to_sitemap(self):
        body = self.client.get("/robots.txt").content.decode()
        self.assertIn("Sitemap: http://testserver/sitemap.xml", body)
        self.assertIn("Disallow: /admin/", body)

    def test_policy_pages(self):
        privacy = self.client.get(reverse("core:privacy"))
        self.assertContains(privacy, "Third-party vendors, including Google, use cookies")
        self.assertEqual(self.client.get(reverse("core:about")).status_code, 200)
        self.assertContains(self.client.get(reverse("core:contact")), "coming soon")
        home = self.client.get(reverse("core:home"))
        self.assertContains(home, reverse("core:privacy"))

    @override_settings(GOOGLE_SITE_VERIFICATION="abc123", CONTACT_EMAIL="hello@lorrank.com")
    def test_verification_tag_and_contact_email(self):
        home = self.client.get(reverse("core:home"))
        self.assertContains(home, '<meta name="google-site-verification" content="abc123">')
        self.assertContains(self.client.get(reverse("core:contact")), "hello@lorrank.com")

    def test_no_verification_tag_by_default(self):
        self.assertNotContains(self.client.get(reverse("core:home")), "google-site-verification")
