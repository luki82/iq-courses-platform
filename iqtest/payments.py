"""
One-off Stripe payments for paid tests (e.g. the $10 Full IQ Assessment).

No account is needed. Paying creates a TestPass with a secret token; the
token is saved in the buyer's browser session and shown to them as a private
link they can bookmark to come back to the test or their result.
"""

import logging

import stripe
from django.conf import settings
from django.db import transaction
from django.urls import reverse
from django.utils import timezone

from .models import TestPass

logger = logging.getLogger(__name__)

SESSION_KEY = "iqtest_pass_tokens"
METADATA_KEY = "test_pass_id"


def _get(obj, key, default=None):
    """Read a field from either a plain dict or a Stripe object."""
    if obj is None:
        return default
    if isinstance(obj, dict):
        return obj.get(key, default)
    return getattr(obj, key, default)


# --- Remembering passes in the visitor's session ---------------------------

def remember_pass(request, test_pass: TestPass) -> None:
    tokens = list(request.session.get(SESSION_KEY, []))
    if test_pass.token not in tokens:
        tokens.append(test_pass.token)
        request.session[SESSION_KEY] = tokens


def passes_in_session(request):
    tokens = request.session.get(SESSION_KEY, [])
    if not tokens:
        return TestPass.objects.none()
    return TestPass.objects.filter(token__in=tokens, status=TestPass.STATUS_PAID)


def unused_pass_for(request, category) -> TestPass | None:
    """The oldest paid, not-yet-used pass this visitor holds for a category."""
    qs = passes_in_session(request).filter(category=category, attempt__isnull=True).order_by("created_at")
    test_pass = qs.first()
    if test_pass is None and request.user.is_authenticated:
        # A logged-in buyer can also use passes bought on another device.
        test_pass = (
            TestPass.objects.filter(
                user=request.user, category=category, status=TestPass.STATUS_PAID, attempt__isnull=True
            )
            .order_by("created_at")
            .first()
        )
        if test_pass:
            remember_pass(request, test_pass)
    return test_pass


# --- Stripe ----------------------------------------------------------------

class CheckoutUnavailable(Exception):
    """Payments aren't configured, or Stripe refused to start a session."""


def start_checkout(request, category) -> str:
    """Create a pending TestPass and a Stripe Checkout session; return its URL."""
    if not settings.STRIPE_SECRET_KEY or not category.price_cents:
        raise CheckoutUnavailable("Payments aren't switched on yet. Please check back soon.")

    stripe.api_key = settings.STRIPE_SECRET_KEY
    user = request.user if request.user.is_authenticated else None
    test_pass = TestPass.objects.create(
        category=category,
        user=user,
        amount_cents=category.price_cents,
        currency=category.currency,
    )

    success_url = request.build_absolute_uri(reverse("iqtest:pass_success"))
    cancel_url = request.build_absolute_uri(reverse("iqtest:test_list"))
    minutes = category.time_limit_minutes
    description = f"One attempt: {category.question_count} questions"
    if minutes:
        description += f", {minutes} minutes"

    try:
        session = stripe.checkout.Session.create(
            mode="payment",
            line_items=[
                {
                    "price_data": {
                        "currency": category.currency,
                        "unit_amount": category.price_cents,
                        "product_data": {"name": f"iQ -- {category.name}", "description": description},
                    },
                    "quantity": 1,
                }
            ],
            customer_email=(user.email or None) if user else None,
            # Stripe replaces {CHECKOUT_SESSION_ID} with the real ID on redirect.
            success_url=f"{success_url}?session_id={{CHECKOUT_SESSION_ID}}",
            cancel_url=cancel_url,
            metadata={METADATA_KEY: test_pass.id, "category": category.slug},
        )
    except stripe.StripeError as exc:
        logger.exception("Stripe checkout session creation failed for test pass %s", test_pass.id)
        test_pass.status = TestPass.STATUS_FAILED
        test_pass.save(update_fields=["status"])
        raise CheckoutUnavailable(
            f"We couldn't start checkout: {exc.user_message or 'please try again shortly.'}"
        ) from exc

    test_pass.stripe_checkout_session_id = session.id
    test_pass.save(update_fields=["stripe_checkout_session_id"])
    return session.url


def is_test_pass_session(session) -> bool:
    return bool(_get(_get(session, "metadata"), METADATA_KEY))


def fulfil_test_pass(session) -> TestPass | None:
    """
    Mark the matching TestPass as paid -- exactly once. Called from both the
    success page and the Stripe webhook; whichever arrives first does the
    work. Returns the pass, or None if this session isn't a paid test pass.
    """
    if _get(session, "payment_status") != "paid":
        return None

    with transaction.atomic():
        test_pass = (
            TestPass.objects.select_for_update()
            .filter(stripe_checkout_session_id=_get(session, "id"))
            .first()
        )
        if test_pass is None:
            return None
        if test_pass.status != TestPass.STATUS_PAID:
            test_pass.status = TestPass.STATUS_PAID
            test_pass.paid_at = timezone.now()
            email = _get(_get(session, "customer_details"), "email") or _get(session, "customer_email") or ""
            test_pass.email = email
            test_pass.save(update_fields=["status", "paid_at", "email"])
    return test_pass
