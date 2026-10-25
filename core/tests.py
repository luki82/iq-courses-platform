from io import StringIO
from django.core.management import call_command
from django.test import TestCase, override_settings
from django.urls import reverse

from core.models import ContactMessage

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
        call_command("seed_english_esl", stdout=StringIO())
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

    def test_contact_email_shown_by_default(self):
        self.assertContains(self.client.get(reverse("core:contact")), "lukiapr9@gmail.com")

    def test_policy_pages(self):
        privacy = self.client.get(reverse("core:privacy"))
        self.assertContains(privacy, "Third-party vendors, including Google, use cookies")
        self.assertEqual(self.client.get(reverse("core:about")).status_code, 200)
        self.assertContains(self.client.get(reverse("core:contact")), "Send message")
        self.assertContains(self.client.get(reverse("core:terms")), "Terms of use")
        home = self.client.get(reverse("core:home"))
        self.assertContains(home, reverse("core:privacy"))

    @override_settings(GOOGLE_SITE_VERIFICATION="abc123", CONTACT_EMAIL="hello@lorrank.com")
    def test_verification_tag_and_contact_email(self):
        home = self.client.get(reverse("core:home"))
        self.assertContains(home, '<meta name="google-site-verification" content="abc123">')
        self.assertContains(self.client.get(reverse("core:contact")), "hello@lorrank.com")

    def test_no_verification_tag_by_default(self):
        self.assertNotContains(self.client.get(reverse("core:home")), "google-site-verification")


@plain_static
class ContactAndAdsTests(TestCase):
    def post(self, **overrides):
        data = {"name": "Amina", "email": "amina@example.com", "topic": "correction",
                "message": "There is a typo in the malaria lesson.", "website": ""}
        data.update(overrides)
        return self.client.post(reverse("core:contact"), data)

    def test_contact_form_saves_message(self):
        response = self.post()
        self.assertRedirects(response, reverse("core:contact"), fetch_redirect_response=False)
        message = ContactMessage.objects.get()
        self.assertEqual((message.name, message.topic, message.is_read), ("Amina", "correction", False))
        # The thank-you message shows on the next page load (a second load uses it up).
        self.assertContains(self.client.get(reverse("core:contact")), "Thanks for your message")

    def test_invalid_form_shows_errors(self):
        response = self.post(email="not-an-email", message="hi")
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "at least 10 characters")
        self.assertEqual(ContactMessage.objects.count(), 0)

    def test_spam_trap_is_silently_dropped(self):
        response = self.post(website="http://spam.example")
        self.assertRedirects(response, reverse("core:contact"))
        self.assertEqual(ContactMessage.objects.count(), 0)

    def test_rate_limit(self):
        for _ in range(4):
            self.post()
        self.assertEqual(ContactMessage.objects.count(), 3)

    def test_ads_txt_missing_until_configured(self):
        self.assertEqual(self.client.get("/ads.txt").status_code, 404)

    @override_settings(ADSENSE_CLIENT_ID="ca-pub-1234567890123456")
    def test_ads_txt_and_adsense_script(self):
        body = self.client.get("/ads.txt").content.decode()
        self.assertEqual(body, "google.com, pub-1234567890123456, DIRECT, f08c47fec0942fa0\n")
        home = self.client.get(reverse("core:home"))
        self.assertContains(home, "adsbygoogle.js?client=ca-pub-1234567890123456")

    def test_no_adsense_script_by_default(self):
        self.assertNotContains(self.client.get(reverse("core:home")), "adsbygoogle")

    def test_navigation_links_to_policy_pages(self):
        home = self.client.get(reverse("core:home")).content.decode()
        for name in ("core:about", "core:contact", "core:privacy", "core:terms"):
            self.assertIn(reverse(name), home)
