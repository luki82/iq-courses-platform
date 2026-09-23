import json

import stripe
from django.conf import settings
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseBadRequest
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.utils import timezone
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST

from .models import Plan, Purchase

stripe.api_key = settings.STRIPE_SECRET_KEY


def pricing(request):
    plans = Plan.objects.filter(is_active=True)
    return render(request, "billing/pricing.html", {"plans": plans})


@login_required
@require_POST
def create_checkout_session(request, slug):
    plan = get_object_or_404(Plan, slug=slug, is_active=True)

    if not settings.STRIPE_SECRET_KEY or not plan.stripe_price_id:
        messages.error(
            request,
            "Payments aren't configured yet. Add STRIPE_SECRET_KEY and a Stripe "
            "price ID on this plan to enable checkout.",
        )
        return redirect("billing:pricing")

    purchase = Purchase.objects.create(user=request.user, plan=plan)

    session = stripe.checkout.Session.create(
        mode="payment",
        payment_method_types=["card"],
        line_items=[{"price": plan.stripe_price_id, "quantity": 1}],
        customer_email=request.user.email or None,
        success_url=request.build_absolute_uri(reverse("billing:checkout_success")),
        cancel_url=request.build_absolute_uri(reverse("billing:checkout_cancel")),
        metadata={"purchase_id": purchase.id, "user_id": request.user.id, "plan_id": plan.id},
    )

    purchase.stripe_checkout_session_id = session.id
    purchase.save(update_fields=["stripe_checkout_session_id"])

    return redirect(session.url, permanent=False)


def checkout_success(request):
    return render(request, "billing/checkout_success.html")


def checkout_cancel(request):
    return render(request, "billing/checkout_cancel.html")


@csrf_exempt
def stripe_webhook(request):
    """
    Stripe calls this URL when a checkout session completes. Point your
    Stripe dashboard webhook at <your-domain>/billing/webhook/ and set
    STRIPE_WEBHOOK_SECRET to the signing secret Stripe gives you for it.
    """
    payload = request.body
    sig_header = request.META.get("HTTP_STRIPE_SIGNATURE", "")

    try:
        if settings.STRIPE_WEBHOOK_SECRET:
            event = stripe.Webhook.construct_event(payload, sig_header, settings.STRIPE_WEBHOOK_SECRET)
        else:
            # Local/dev fallback when no webhook secret is configured yet.
            event = json.loads(payload)
    except ValueError:
        return HttpResponseBadRequest("Invalid payload")
    except Exception:
        # Covers stripe's signature-verification error, whichever module path
        # the installed stripe SDK version exposes it under.
        return HttpResponseBadRequest("Invalid signature")

    event_type = event["type"] if isinstance(event, dict) else event.type
    data_object = event["data"]["object"] if isinstance(event, dict) else event.data.object

    if event_type == "checkout.session.completed":
        session_id = data_object["id"] if isinstance(data_object, dict) else data_object.id
        try:
            purchase = Purchase.objects.select_related("user", "plan").get(
                stripe_checkout_session_id=session_id
            )
        except Purchase.DoesNotExist:
            return HttpResponse(status=200)

        purchase.status = Purchase.STATUS_PAID
        purchase.completed_at = timezone.now()
        purchase.save(update_fields=["status", "completed_at"])

        if purchase.plan:
            purchase.user.profile.grant_premium(purchase.plan.duration_days)

    return HttpResponse(status=200)
