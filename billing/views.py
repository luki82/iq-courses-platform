"""
Donations.

Everything on iQ is free. Visitors who want to help keep the site online can
give a one-off donation through Stripe Checkout. No account is needed, and
nothing is unlocked by donating. Each donation shows up in your Stripe
dashboard (Payments), with "iQ donation" as the description.
"""
import json
import logging
from decimal import Decimal, InvalidOperation

import stripe
from django.conf import settings
from django.contrib import messages
from django.http import HttpResponse, HttpResponseBadRequest
from django.shortcuts import redirect, render
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST

from iqtest import payments as iq_payments

logger = logging.getLogger(__name__)

DONATION_CURRENCY = "aud"
PRESET_AMOUNTS = [5, 10, 20, 50]  # whole dollars, shown as quick-pick buttons
MIN_AMOUNT = Decimal("2")
MAX_AMOUNT = Decimal("1000")


def _get(obj, key, default=None):
    """Read a field from either a plain dict or a Stripe object."""
    if obj is None:
        return default
    if isinstance(obj, dict):
        return obj.get(key, default)
    return getattr(obj, key, default)


def donate(request):
    return render(
        request,
        "billing/donate.html",
        {
            "preset_amounts": PRESET_AMOUNTS,
            "min_amount": MIN_AMOUNT,
            "max_amount": MAX_AMOUNT,
            "donations_enabled": bool(settings.STRIPE_SECRET_KEY),
        },
    )


def _parse_amount(raw) -> Decimal | None:
    """Turn the submitted amount (e.g. '10' or '7.50') into dollars, or None if invalid."""
    try:
        amount = Decimal(str(raw).strip().lstrip("$")).quantize(Decimal("0.01"))
    except (InvalidOperation, ValueError):
        return None
    if not amount.is_finite() or amount < MIN_AMOUNT or amount > MAX_AMOUNT:
        return None
    return amount


@require_POST
def donate_checkout(request):
    if not settings.STRIPE_SECRET_KEY:
        messages.error(request, "Donations aren't switched on yet. Thank you for wanting to help!")
        return redirect("billing:donate")

    # A custom amount, if typed in, wins over the quick-pick buttons.
    amount = _parse_amount(request.POST.get("custom_amount") or request.POST.get("amount", ""))
    if amount is None:
        messages.error(request, f"Please choose an amount between ${MIN_AMOUNT} and ${MAX_AMOUNT}.")
        return redirect("billing:donate")

    stripe.api_key = settings.STRIPE_SECRET_KEY
    try:
        session = stripe.checkout.Session.create(
            mode="payment",
            submit_type="donate",
            line_items=[
                {
                    "price_data": {
                        "currency": DONATION_CURRENCY,
                        "unit_amount": int(amount * 100),
                        "product_data": {
                            "name": "Donation to iQ",
                            "description": "Helps keep free courses and IQ tests online at lorrank.com",
                        },
                    },
                    "quantity": 1,
                }
            ],
            customer_email=(request.user.email or None) if request.user.is_authenticated else None,
            payment_intent_data={"description": "iQ donation"},
            success_url=request.build_absolute_uri(reverse("billing:donate_thanks")),
            cancel_url=request.build_absolute_uri(reverse("billing:donate")),
            metadata={"kind": "donation"},
        )
    except stripe.StripeError as exc:
        logger.exception("Stripe donation checkout failed")
        messages.error(request, f"We couldn't start the donation: {exc.user_message or 'please try again shortly.'}")
        return redirect("billing:donate")

    return redirect(session.url, permanent=False)


def donate_thanks(request):
    return render(request, "billing/donate_thanks.html")


def pricing(request):
    """The old Premium page. Everything is free now, so send visitors to Donate."""
    return redirect("billing:donate", permanent=True)


@csrf_exempt
@require_POST
def stripe_webhook(request):
    """
    Stripe calls this URL when a checkout session completes. Donations need
    no follow-up (Stripe keeps the record), so this only finishes off any IQ
    test pass that was bought just before tests became free.
    """
    payload = request.body
    sig_header = request.META.get("HTTP_STRIPE_SIGNATURE", "")

    if settings.STRIPE_WEBHOOK_SECRET:
        try:
            event = stripe.Webhook.construct_event(payload, sig_header, settings.STRIPE_WEBHOOK_SECRET)
        except ValueError:
            return HttpResponseBadRequest("Invalid payload")
        except stripe.SignatureVerificationError:
            return HttpResponseBadRequest("Invalid signature")
    elif settings.DEBUG:
        # Local development only: accept unsigned events so you can test
        # without the Stripe CLI. Never reached in production (DEBUG=False).
        try:
            event = json.loads(payload)
        except ValueError:
            return HttpResponseBadRequest("Invalid payload")
    else:
        logger.error("Stripe webhook received but STRIPE_WEBHOOK_SECRET is not set; ignoring it.")
        return HttpResponse("Webhook secret not configured", status=503)

    event_type = _get(event, "type")
    data_object = _get(_get(event, "data"), "object")

    if event_type in ("checkout.session.completed", "checkout.session.async_payment_succeeded"):
        if iq_payments.is_test_pass_session(data_object):
            iq_payments.fulfil_test_pass(data_object)

    return HttpResponse(status=200)
