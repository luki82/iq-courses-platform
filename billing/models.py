from django.conf import settings
from django.db import models


class Plan(models.Model):
    """A purchasable premium plan. Configure the matching Price in your Stripe dashboard."""

    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True)
    description = models.CharField(max_length=255, blank=True)
    price_display = models.CharField(max_length=50, help_text="Display only, e.g. '$9.99/month'.")
    stripe_price_id = models.CharField(
        max_length=255, blank=True, help_text="Price ID from Stripe (looks like price_...)."
    )
    duration_days = models.PositiveIntegerField(
        default=30, help_text="How many days of premium access one purchase grants."
    )
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ["duration_days"]

    def __str__(self):
        return self.name


class Purchase(models.Model):
    STATUS_PENDING = "pending"
    STATUS_PAID = "paid"
    STATUS_FAILED = "failed"
    STATUS_CHOICES = [
        (STATUS_PENDING, "Pending"),
        (STATUS_PAID, "Paid"),
        (STATUS_FAILED, "Failed"),
    ]

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="purchases")
    plan = models.ForeignKey(Plan, on_delete=models.SET_NULL, null=True)
    stripe_checkout_session_id = models.CharField(max_length=255, blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default=STATUS_PENDING)
    created_at = models.DateTimeField(auto_now_add=True)
    completed_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.user} - {self.plan} - {self.status}"
