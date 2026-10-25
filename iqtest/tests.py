from io import StringIO
import time
from types import SimpleNamespace
from unittest import mock

from django.contrib.auth import get_user_model
from django.core.management import call_command
from django.test import TestCase, override_settings
from django.urls import reverse

from iqtest.models import Category, TestAttempt, TestPass
from iqtest.views import _start_key

SLUG = "full-iq-assessment"

# Render pages without needing `collectstatic` first.
plain_static = override_settings(
    STORAGES={
        "default": {"BACKEND": "django.core.files.storage.FileSystemStorage"},
        "staticfiles": {"BACKEND": "django.contrib.staticfiles.storage.StaticFilesStorage"},
    }
)


@plain_static
class FreeTestFlowTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        call_command("seed_full_iq_test", stdout=StringIO())
        cls.category = Category.objects.get(slug=SLUG)

    def all_correct(self):
        return {
            f"question_{q.id}": q.choices.get(is_correct=True).id
            for q in self.category.questions.prefetch_related("choices")
        }

    def test_seeded_test_has_no_price(self):
        self.assertIsNone(self.category.price_cents)

    def test_list_page_says_free_and_has_no_payment(self):
        html = self.client.get(reverse("iqtest:test_list")).content.decode()
        self.assertIn("Free", html)
        self.assertIn("How it works", html)
        self.assertIn(reverse("iqtest:take_test", args=[SLUG]), html)
        self.assertNotIn("$10", html)
        self.assertNotIn("Stripe", html)
        self.assertNotIn("Premium", html)

    def test_guest_takes_test_and_sees_full_result(self):
        page = self.client.get(reverse("iqtest:take_test", args=[SLUG]))
        self.assertEqual(page.status_code, 200)
        self.assertEqual(page.context["remaining_seconds"], 1800)

        response = self.client.post(reverse("iqtest:take_test", args=[SLUG]), self.all_correct())
        attempt = TestAttempt.objects.get()
        self.assertRedirects(response, reverse("iqtest:result_detail", args=[attempt.pk]))
        self.assertIsNone(attempt.user)
        self.assertEqual((attempt.score, attempt.total_questions), (30, 30))
        self.assertTrue(attempt.detail_unlocked)
        self.assertIsNotNone(attempt.iq_score)

        result = self.client.get(reverse("iqtest:result_detail", args=[attempt.pk]))
        self.assertContains(result, "30 / 30")
        self.assertContains(result, "Answer breakdown")
        self.assertContains(result, "Estimated IQ score")
        self.assertNotContains(result, "Premium")

    def test_test_can_be_retaken(self):
        for _ in range(2):
            self.client.get(reverse("iqtest:take_test", args=[SLUG]))
            self.client.post(reverse("iqtest:take_test", args=[SLUG]), self.all_correct())
        self.assertEqual(TestAttempt.objects.count(), 2)

    def test_refresh_does_not_reset_clock(self):
        self.client.get(reverse("iqtest:take_test", args=[SLUG]))
        session = self.client.session
        session[_start_key(self.category)] = time.time() - 600
        session.save()
        page = self.client.get(reverse("iqtest:take_test", args=[SLUG]))
        self.assertAlmostEqual(page.context["remaining_seconds"], 1200, delta=2)

    def test_late_answers_are_not_counted(self):
        self.client.get(reverse("iqtest:take_test", args=[SLUG]))
        session = self.client.session
        session[_start_key(self.category)] = time.time() - 40 * 60
        session.save()
        self.client.post(reverse("iqtest:take_test", args=[SLUG]), self.all_correct())
        attempt = TestAttempt.objects.get()
        self.assertEqual(attempt.score, 0)
        self.assertEqual(attempt.time_taken_seconds, 1800)

    def test_stranger_cannot_see_guest_result(self):
        self.client.get(reverse("iqtest:take_test", args=[SLUG]))
        self.client.post(reverse("iqtest:take_test", args=[SLUG]), self.all_correct())
        attempt = TestAttempt.objects.get()
        stranger = self.client_class()
        self.assertEqual(stranger.get(reverse("iqtest:result_detail", args=[attempt.pk])).status_code, 404)

    def test_logged_in_user_owns_result_on_any_device(self):
        user = get_user_model().objects.create_user("member", "member@example.com", "pw-12345-x")
        self.client.force_login(user)
        self.client.get(reverse("iqtest:take_test", args=[SLUG]))
        self.client.post(reverse("iqtest:take_test", args=[SLUG]), self.all_correct())
        attempt = TestAttempt.objects.get()
        self.assertEqual(attempt.user, user)

        other_device = self.client_class()
        other_device.force_login(user)
        self.assertEqual(other_device.get(reverse("iqtest:result_detail", args=[attempt.pk])).status_code, 200)

    def test_old_buy_button_goes_straight_to_test(self):
        response = self.client.post(reverse("iqtest:buy_pass", args=[SLUG]))
        self.assertRedirects(response, reverse("iqtest:take_test", args=[SLUG]))

    def test_old_paid_test_is_free_even_if_price_still_in_database(self):
        Category.objects.filter(pk=self.category.pk).update(price_cents=1000, is_premium=True)
        self.assertEqual(self.client.get(reverse("iqtest:take_test", args=[SLUG])).status_code, 200)


@plain_static
class OldPassHolderTests(TestCase):
    """People who paid before tests went free keep their private links."""

    @classmethod
    def setUpTestData(cls):
        call_command("seed_full_iq_test", stdout=StringIO())
        cls.category = Category.objects.get(slug=SLUG)

    def make_pass(self, **kwargs):
        return TestPass.objects.create(
            category=self.category, amount_cents=1000, currency="aud", status=TestPass.STATUS_PAID, **kwargs
        )

    def test_unused_pass_link_opens_test(self):
        test_pass = self.make_pass()
        response = self.client.get(reverse("iqtest:pass_detail", args=[test_pass.token]))
        self.assertRedirects(response, reverse("iqtest:take_test", args=[SLUG]))

    def test_used_pass_link_shows_result_on_new_device(self):
        attempt = TestAttempt.objects.create(category=self.category, score=20, total_questions=30, detail_unlocked=True)
        test_pass = self.make_pass(attempt=attempt)
        response = self.client.get(reverse("iqtest:pass_detail", args=[test_pass.token]))
        self.assertRedirects(response, reverse("iqtest:result_detail", args=[attempt.pk]))
        self.assertContains(self.client.get(response.url), "20 / 30")

    def test_unknown_pass_link_is_404(self):
        response = self.client.get(reverse("iqtest:pass_detail", args=["not-a-real-token"]))
        self.assertEqual(response.status_code, 404)

    @override_settings(STRIPE_WEBHOOK_SECRET="", DEBUG=True)
    def test_webhook_still_records_in_flight_pass_payment(self):
        test_pass = TestPass.objects.create(
            category=self.category, amount_cents=1000, currency="aud", stripe_checkout_session_id="cs_test_1"
        )
        session = {
            "id": "cs_test_1",
            "payment_status": "paid",
            "customer_details": {"email": "buyer@example.com"},
            "metadata": {"test_pass_id": str(test_pass.id)},
        }
        event = {"type": "checkout.session.completed", "data": {"object": session}}
        response = self.client.post(reverse("billing:stripe_webhook"), event, content_type="application/json")
        self.assertEqual(response.status_code, 200)
        test_pass.refresh_from_db()
        self.assertTrue(test_pass.is_paid)

    def test_previously_locked_result_is_unlocked(self):
        user = get_user_model().objects.create_user("old", "old@example.com", "pw-12345-x")
        attempt = TestAttempt.objects.create(
            user=user, category=self.category, score=15, total_questions=30, detail_unlocked=False
        )
        self.client.force_login(user)
        result = self.client.get(reverse("iqtest:result_detail", args=[attempt.pk]))
        self.assertContains(result, "Estimated IQ score")
        attempt.refresh_from_db()
        self.assertTrue(attempt.detail_unlocked)
        self.assertEqual(attempt.iq_score, 100)


@plain_static
class PracticeTestTests(TestCase):
    def test_former_premium_category_is_open_to_guests(self):
        call_command("seed_iqtest", stdout=StringIO())
        for slug in ("logical-reasoning", "numerical-advanced"):
            category = Category.objects.get(slug=slug)
            Category.objects.filter(pk=category.pk).update(is_premium=True)
            if category.questions.exists():
                self.assertEqual(self.client.get(reverse("iqtest:take_test", args=[slug])).status_code, 200)


@plain_static
@override_settings(STRIPE_SECRET_KEY="sk_test_dummy", DONATIONS_ENABLED=True)
class DonationTests(TestCase):
    def test_donate_page(self):
        response = self.client.get(reverse("billing:donate"))
        self.assertContains(response, "Help keep iQ free")
        self.assertContains(response, 'value="10"')

    def test_old_pricing_page_redirects_to_donate(self):
        response = self.client.get(reverse("billing:pricing"))
        self.assertRedirects(response, reverse("billing:donate"), status_code=301)

    def donate(self, data):
        created = SimpleNamespace(id="cs_test_donation", url="https://checkout.stripe.test/donate")
        with mock.patch("stripe.checkout.Session.create", return_value=created) as create:
            response = self.client.post(reverse("billing:donate_checkout"), data)
        return response, create

    def test_preset_amount_starts_stripe_checkout(self):
        response, create = self.donate({"amount": "20"})
        self.assertRedirects(response, "https://checkout.stripe.test/donate", fetch_redirect_response=False)
        kwargs = create.call_args.kwargs
        self.assertEqual(kwargs["submit_type"], "donate")
        self.assertEqual(kwargs["line_items"][0]["price_data"]["unit_amount"], 2000)
        self.assertEqual(kwargs["line_items"][0]["price_data"]["currency"], "aud")
        self.assertEqual(kwargs["metadata"], {"kind": "donation"})

    def test_custom_amount_wins(self):
        _, create = self.donate({"amount": "10", "custom_amount": "7.50"})
        self.assertEqual(create.call_args.kwargs["line_items"][0]["price_data"]["unit_amount"], 750)

    def test_bad_amounts_are_rejected(self):
        for bad in ("1", "abc", "5000", "-5", "nan", "inf", ""):
            response, create = self.donate({"custom_amount": bad} if bad else {})
            self.assertRedirects(response, reverse("billing:donate"))
            create.assert_not_called()

    @override_settings(STRIPE_SECRET_KEY="")
    @override_settings(DONATIONS_ENABLED=False)
    def test_switched_off_even_with_stripe_key(self):
        self.assertContains(self.client.get(reverse("billing:donate")), "Online donations are being set up")
        response, create = self.donate({"amount": "10"})
        self.assertRedirects(response, reverse("billing:donate"))
        create.assert_not_called()

    def test_without_stripe_key_page_says_coming_soon(self):
        self.assertContains(self.client.get(reverse("billing:donate")), "being set up")
        response, create = self.donate({"amount": "10"})
        self.assertRedirects(response, reverse("billing:donate"))
        create.assert_not_called()

    def test_thanks_page(self):
        self.assertContains(self.client.get(reverse("billing:donate_thanks")), "Thank you")

    @override_settings(STRIPE_WEBHOOK_SECRET="", DEBUG=True)
    def test_webhook_ignores_donations(self):
        event = {
            "type": "checkout.session.completed",
            "data": {"object": {"id": "cs_d", "payment_status": "paid", "metadata": {"kind": "donation"}}},
        }
        response = self.client.post(reverse("billing:stripe_webhook"), event, content_type="application/json")
        self.assertEqual(response.status_code, 200)
