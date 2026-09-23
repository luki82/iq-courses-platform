from datetime import timedelta

from django.conf import settings
from django.db import models
from django.utils import timezone


class Profile(models.Model):
    """
    Extra data attached to every user, including their free/premium access
    status. A Profile is created automatically for every new User (see
    signals.py) so code can always assume ``request.user.profile`` exists
    for an authenticated user.
    """

    user = models.OneToOneField(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="profile"
    )
    bio = models.CharField(max_length=255, blank=True)

    # Premium access. is_premium is flipped on by a successful purchase
    # (see billing.views) and off again once premium_until passes.
    is_premium = models.BooleanField(default=False)
    premium_until = models.DateTimeField(
        null=True,
        blank=True,
        help_text="If set, premium access expires at this time. Leave blank for unlimited premium.",
    )

    # Freemium usage counters.
    free_test_attempts_used = models.PositiveIntegerField(default=0)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Profile<{self.user.username}>"

    @property
    def has_premium_access(self) -> bool:
        """True if the user currently has paid access."""
        if not self.is_premium:
            return False
        if self.premium_until is None:
            return True
        return self.premium_until >= timezone.now()

    def grant_premium(self, duration_days: int | None):
        """Activate (or extend) premium access. duration_days=None means unlimited."""
        self.is_premium = True
        if duration_days is None:
            self.premium_until = None
        else:
            base = self.premium_until if (self.premium_until and self.premium_until >= timezone.now()) else timezone.now()
            self.premium_until = base + timedelta(days=duration_days)
        self.save(update_fields=["is_premium", "premium_until"])
