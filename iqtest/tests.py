from datetime import timedelta
from types import SimpleNamespace
from unittest import mock

from django.contrib.auth import get_user_model
from django.core.management import call_command
from django.test import TestCase, override_settings
from django.urls import reverse
from django.utils import timezone

from iqtest.models import Category, TestAttempt, TestPass

SLUG = "full-iq-assessment"


def fake_session(test_pass, paid=True, email="buyer@example.com"):
    return {
        "id": test_pass.stripe_checkout_session_id,
        "payment_status": "paid" if paid else "unpaid",
        "customer_details": {"email": email},
        "metadata": {"test_pass_id": str(test_pass.id)},
    }


@override_settings(STRIPE_SECRET_KEY="sk_test_dummy", STRIPE_WEBHOOK_SECRET="", DEBUG=True)
class PaidTestFlowTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        call_command("seed_full_iq_test", stdout=open("/dev/null", "w"))
        cls.category = Category.objects.get(slug=SLUG)

    def buy(self, client=None):
        client = client or self.client
        created = SimpleNamespace(id=f"cs_test_{TestPass.objects.count() + 1}", url="https://checkout.stripe.test/pay")
        with mock.patch("stripe.checkout.Session.create", return_value=created) as create:
            response = client.post(reverse("iqtest:buy_pass", args=[SLUG]))
        self.assertRedirects(response, created.url, fetch_redirect_response=False)
        kwargs = create.call_args.kwargs
        self.assertEqual(kwargs["line_items"][0]["price_data"]["unit_amount"], 1000)
        self.assertEqual(kwargs["line_items"][0]["price_data"]["currency"], "aud")
        return TestPass.objects.get(stripe_checkout_session_id=created.id)

    def pay(self, test_pass, client=None):
        client = client or self.client
        with mock.patch("stripe.checkout.Session.retrieve", return_value=fake_session(test_pass)):
            response = client.get(reverse("iqtest:pass_success") + f"?session_id={test_pass.stripe_checkout_session_id}")
        self.assertRedirects(response, reverse("iqtest:pass_detail", args=[test_pass.token]))
        test_pass.refresh_from_db()
        return test_pass

    def all_correct(self):
        return {
            f"question_{q.id}": q.choices.get(is_correct=True).id
            for q in self.category.questions.prefetch_related("choices")
        }

    def test_list_page_describes_process_and_price(self):
        html = self.client.get(reverse("iqtest:test_list")).content.decode()
        self.assertIn("$10 AUD", html)
        self.assertIn("How it works", html)
        self.assertIn("one attempt", html)
        self.assertNotIn("seed_iqtest", html)

    def test_guest_cannot_take_test_without_paying(self):
        response = self.client.get(reverse("iqtest:take_test", args=[SLUG]))
        self.assertRedirects(response, reverse("iqtest:test_list"))

    def test_guest_full_flow(self):
        test_pass = self.buy()
        self.assertEqual(test_pass.status, TestPass.STATUS_PENDING)
        self.assertIsNone(test_pass.user)

        test_pass = self.pay(test_pass)
        self.assertTrue(test_pass.is_paid)
        self.assertEqual(test_pass.email, "buyer@example.com")

        detail = self.client.get(reverse("iqtest:pass_detail", args=[test_pass.token]))
        self.assertContains(detail, test_pass.token)
        self.assertContains(detail, "Start the test now")

        page = self.client.get(reverse("iqtest:take_test", args=[SLUG]))
        self.assertEqual(page.status_code, 200)
        self.assertEqual(page.context["remaining_seconds"], 1800)
        test_pass.refresh_from_db()
        self.assertIsNotNone(test_pass.started_at)

        response = self.client.post(reverse("iqtest:take_test", args=[SLUG]), self.all_correct())
        attempt = TestAttempt.objects.get()
        self.assertRedirects(response, reverse("iqtest:result_detail", args=[attempt.pk]))
        self.assertIsNone(attempt.user)
        self.assertEqual((attempt.score, attempt.total_questions), (30, 30))
        self.assertTrue(attempt.detail_unlocked)
        self.assertIsNotNone(attempt.iq_score)

        result = self.client.get(reverse("iqtest:result_detail", args=[attempt.pk]))
        self.assertContains(result, "30 / 30")
        self.assertContains(result, test_pass.token)

        # One attempt only: going back to the test now shows the result.
        again = self.client.get(reverse("iqtest:take_test", args=[SLUG]))
        self.assertRedirects(again, reverse("iqtest:result_detail", args=[attempt.pk]))

    def test_double_submit_creates_one_attempt(self):
        test_pass = self.pay(self.buy())
        self.client.get(reverse("iqtest:take_test", args=[SLUG]))
        self.client.post(reverse("iqtest:take_test", args=[SLUG]), self.all_correct())
        self.client.post(reverse("iqtest:take_test", args=[SLUG]), self.all_correct())
        self.assertEqual(TestAttempt.objects.count(), 1)
        test_pass.refresh_from_db()
        self.assertTrue(test_pass.is_used)

    def test_refresh_does_not_reset_clock(self):
        test_pass = self.pay(self.buy())
        self.client.get(reverse("iqtest:take_test", args=[SLUG]))
        TestPass.objects.filter(pk=test_pass.pk).update(started_at=timezone.now() - timedelta(minutes=10))
        page = self.client.get(reverse("iqtest:take_test", args=[SLUG]))
        self.assertEqual(page.context["remaining_seconds"], 1200)

    def test_late_answers_are_not_counted(self):
        test_pass = self.pay(self.buy())
        self.client.get(reverse("iqtest:take_test", args=[SLUG]))
        TestPass.objects.filter(pk=test_pass.pk).update(started_at=timezone.now() - timedelta(minutes=40))
        self.client.post(reverse("iqtest:take_test", args=[SLUG]), self.all_correct())
        attempt = TestAttempt.objects.get()
        self.assertEqual(attempt.score, 0)
        self.assertEqual(attempt.time_taken_seconds, 1800)

    def test_private_link_restores_access_on_another_device(self):
        test_pass = self.pay(self.buy())
        other_device = self.client_class()
        self.assertRedirects(
            other_device.get(reverse("iqtest:take_test", args=[SLUG])), reverse("iqtest:test_list")
        )
        other_device.get(reverse("iqtest:pass_detail", args=[test_pass.token]))
        self.assertEqual(other_device.get(reverse("iqtest:take_test", args=[SLUG])).status_code, 200)

    def test_stranger_cannot_see_result(self):
        test_pass = self.pay(self.buy())
        self.client.get(reverse("iqtest:take_test", args=[SLUG]))
        self.client.post(reverse("iqtest:take_test", args=[SLUG]), self.all_correct())
        attempt = TestAttempt.objects.get()
        stranger = self.client_class()
        self.assertEqual(stranger.get(reverse("iqtest:result_detail", args=[attempt.pk])).status_code, 404)

    def test_unknown_pass_link_is_404(self):
        response = self.client.get(reverse("iqtest:pass_detail", args=["not-a-real-token"]))
        self.assertEqual(response.status_code, 404)

    def test_unpaid_session_does_not_grant_access(self):
        test_pass = self.buy()
        with mock.patch("stripe.checkout.Session.retrieve", return_value=fake_session(test_pass, paid=False)):
            response = self.client.get(
                reverse("iqtest:pass_success") + f"?session_id={test_pass.stripe_checkout_session_id}"
            )
        self.assertContains(response, "Confirming your payment")
        self.assertRedirects(
            self.client.get(reverse("iqtest:take_test", args=[SLUG])), reverse("iqtest:test_list")
        )

    def test_webhook_marks_pass_paid(self):
        test_pass = self.buy()
        event = {"type": "checkout.session.completed", "data": {"object": fake_session(test_pass)}}
        response = self.client.post(reverse("billing:stripe_webhook"), event, content_type="application/json")
        self.assertEqual(response.status_code, 200)
        test_pass.refresh_from_db()
        self.assertTrue(test_pass.is_paid)
        # The success page afterwards still works (already fulfilled).
        self.pay(test_pass)

    def test_logged_in_buyer_is_linked_and_owns_result(self):
        user = get_user_model().objects.create_user("member", "member@example.com", "pw-12345-x")
        self.client.force_login(user)
        test_pass = self.pay(self.buy())
        self.assertEqual(test_pass.user, user)
        self.client.get(reverse("iqtest:take_test", args=[SLUG]))
        self.client.post(reverse("iqtest:take_test", args=[SLUG]), self.all_correct())
        attempt = TestAttempt.objects.get()
        self.assertEqual(attempt.user, user)
        # Free quota isn't used up by a paid test.
        user.profile.refresh_from_db()
        self.assertEqual(user.profile.free_test_attempts_used, 0)

    def test_paying_twice_reuses_unused_pass(self):
        test_pass = self.pay(self.buy())
        response = self.client.post(reverse("iqtest:buy_pass", args=[SLUG]))
        self.assertRedirects(response, reverse("iqtest:pass_detail", args=[test_pass.token]))
        self.assertEqual(TestPass.objects.count(), 1)


class MemberTestStillWorksTests(TestCase):
    def test_free_category_still_needs_login(self):
        call_command("seed_iqtest", stdout=open("/dev/null", "w"))
        response = self.client.get(reverse("iqtest:take_test", args=["logical-reasoning"]))
        self.assertEqual(response.status_code, 302)
        self.assertIn(reverse("accounts:login"), response.url)
