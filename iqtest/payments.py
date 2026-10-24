"""
Leftovers from when the Full IQ Assessment was a paid test.

Every test is free now, so nothing here sells anything. It stays so that
people who already bought a pass keep access to their result through their
private link, and so a payment that was still in flight when tests went free
is recorded properly when Stripe's webhook arrives.
"""

import logging

from django.db import transaction
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
