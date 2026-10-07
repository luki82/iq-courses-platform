import json
import logging

import stripe
from django.conf import settings
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.http import HttpResponse, HttpResponseBadRequest
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.utils import timezone
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST

from .models import Plan, Purchase

logger = logging.getLogger(__name__)

stripe.api_key = settings.STRIPE_SECRET_KEY


def _get(obj, key, default=None):
    """Read a field from either a plain dict or a Stripe object."""
    if isinstance(obj, dict):
        return obj.get(key, default)
    return getattr(obj, key, default)


def fulfil_checkout_session(session) -> Purchase | None:
    """
    Mark the matching Purchase as paid and grant Premium -- exactly once.

    Called from both the webhook and the success page, so whichever arrives
    first does the work and the other is a no-op. Returns the Purchase, or
    None if the session isn't ours or isn't paid yet.
    """
    if _get(session, "payment_status") != "paid":
        return None

    with transaction.atomic():
        purchase = (
            Purchase.objects.select_for_update()
            .select_related("user", "plan")
            .filter(stripe_checkout_session_id=_get(session, "id"))
            .first()
        )
        if purchase is None:
            return None
        if purchase.status == Purchase.STATUS_PAID:
            return purchase  # already fulfilled (Stripe retries, or success page got there first)

        purchase.status = Purchase.STATUS_PAID
        purchase.completed_at = timezone.now()
        purchase.save(update_fields=["status", "completed_at"])

        if purchase.plan:
            purchase.user.profile.grant_premium(purchase.plan.duration_days)

    return purchase


def pricing(request):
    plans = Plan.objects.filter(is_active=True)
    has_premium = request.user.is_authenticated and request.user.profile.has_premium_access
    return render(
        request,
        "billing/pricing.html",
        {"plans": plans, "has_premium": has_premium, "premium_until": has_premium and request.user.profile.premium_until},
    )


@login_required
@require_POST
def create_checkout_session(request, slug):
    plan = get_object_or_404(Plan, slug=slug, is_active=True)

    if not settings.STRIPE_SECRET_KEY or not (plan.stripe_price_id or plan.price_cents):
        messages.error(
            request,
            "Payments aren't switched on yet. Please check back soon.",
        )
        return redirect("billing:pricing")

    if plan.stripe_price_id:
        line_item = {"price": plan.stripe_price_id, "quantity": 1}
    else:
        line_item = {
            "price_data": {
                "currency": plan.currency,
                "unit_amount": plan.price_cents,
                "product_data": {
                    "name": f"iQ Premium -- {plan.name}",
                    "description": plan.description or f"{plan.duration_days} days of Premium access",
                },
            },
            "quantity": 1,
        }

    purchase = Purchase.objects.create(user=request.user, plan=plan)

    success_url = request.build_absolute_uri(reverse("billing:checkout_success"))
    try:
        session = stripe.checkout.Session.create(
            mode="payment",
            line_items=[line_item],
            customer_email=request.user.email or None,
            client_reference_id=str(request.user.id),
            # Stripe replaces {CHECKOUT_SESSION_ID} with the real ID on redirect.
            success_url=f"{success_url}?session_id={{CHECKOUT_SESSION_ID}}",
            cancel_url=request.build_absolute_uri(reverse("billing:checkout_cancel")),
            metadata={"purchase_id": purchase.id, "user_id": request.user.id, "plan_id": plan.id},
        )
    except stripe.StripeError as exc:
        logger.exception("Stripe checkout session creation failed")
        purchase.status = Purchase.STATUS_FAILED
        purchase.save(update_fields=["status"])
        messages.error(request, f"We couldn't start checkout: {exc.user_message or 'please try again shortly.'}")
        return redirect("billing:pricing")

    purchase.stripe_checkout_session_id = session.id
    purchase.save(update_fields=["stripe_checkout_session_id"])

    return redirect(session.url, permanent=False)


def checkout_success(request):
    """
    Stripe redirects here after payment. We confirm the session with Stripe
    directly so access is granted straight away, even if the webhook is
    delayed. The webhook remains the backstop if the user closes the tab.
    """
    confirmed = False
    session_id = request.GET.get("session_id", "")
    if session_id and settings.STRIPE_SECRET_KEY:
        try:
            session = stripe.checkout.Session.retrieve(session_id)
            purchase = fulfil_checkout_session(session)
            confirmed = purchase is not None and (
                not request.user.is_authenticated or purchase.user_id == request.user.id
            )
        except stripe.StripeError:
            logger.exception("Could not retrieve checkout session %s", session_id)
    return render(request, "billing/checkout_success.html", {"confirmed": confirmed})


def checkout_cancel(request):
    return render(request, "billing/checkout_cancel.html")


@csrf_exempt
@require_POST
def stripe_webhook(request):
    """
    Stripe calls this URL when a checkout session completes. Point your
    Stripe dashboard webhook at <your-domain>/billing/webhook/ and set
    STRIPE_WEBHOOK_SECRET to the signing secret Stripe gives you for it.
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
        fulfil_checkout_session(data_object)

    return HttpResponse(status=200)
