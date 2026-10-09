import secrets

from django.conf import settings
from django.db import models


class Category(models.Model):
    """A themed set of questions, e.g. 'Logical Reasoning' or 'Numerical'."""

    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(unique=True)
    description = models.TextField(blank=True)
    is_premium = models.BooleanField(
        default=False, help_text="If set, only users with premium access can attempt this category at all."
    )
    time_limit_minutes = models.PositiveIntegerField(
        null=True,
        blank=True,
        help_text="Countdown length for this test. Leave blank for an untimed test.",
    )
    price_cents = models.PositiveIntegerField(
        null=True,
        blank=True,
        help_text=(
            "One-off price in cents for a single attempt (e.g. 1000 = $10). When set, "
            "anyone -- logged in or not -- must buy a test pass to take this test. "
            "Leave blank for the normal free/Premium rules."
        ),
    )
    currency = models.CharField(max_length=3, default="aud", help_text="Three-letter currency code, e.g. aud.")

    class Meta:
        verbose_name_plural = "categories"
        ordering = ["name"]

    def __str__(self):
        return self.name

    @property
    def question_count(self):
        return self.questions.count()

    @property
    def is_paid_test(self) -> bool:
        return bool(self.price_cents)

    @property
    def price_display(self) -> str:
        if not self.price_cents:
            return ""
        dollars, cents = divmod(self.price_cents, 100)
        amount = f"${dollars}" if cents == 0 else f"${dollars}.{cents:02d}"
        return f"{amount} {self.currency.upper()}"


class Question(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name="questions")
    text = models.TextField()
    image = models.ImageField(upload_to="iqtest/questions/", blank=True, null=True)
    order = models.PositiveIntegerField(default=0)
    explanation = models.TextField(
        blank=True, help_text="Shown after the test, to users who have detail unlocked."
    )

    class Meta:
        ordering = ["order", "id"]

    def __str__(self):
        return self.text[:60]


class Choice(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name="choices")
    text = models.CharField(max_length=255)
    is_correct = models.BooleanField(default=False)

    def __str__(self):
        return self.text


class TestAttempt(models.Model):
    # Blank for guests who bought a test pass without an account.
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="test_attempts",
        null=True,
        blank=True,
    )
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name="attempts")
    started_at = models.DateTimeField(auto_now_add=True)
    completed_at = models.DateTimeField(null=True, blank=True)
    score = models.PositiveIntegerField(default=0)
    total_questions = models.PositiveIntegerField(default=0)
    iq_score = models.PositiveIntegerField(null=True, blank=True)
    time_taken_seconds = models.PositiveIntegerField(null=True, blank=True)

    # Whether this particular attempt's full breakdown (explanations,
    # IQ score) is unlocked. Decided once, at submission time, from the
    # user's premium status / remaining free quota at that moment.
    detail_unlocked = models.BooleanField(default=False)

    class Meta:
        ordering = ["-started_at"]

    @property
    def time_taken_display(self) -> str:
        if self.time_taken_seconds is None:
            return ""
        minutes, seconds = divmod(self.time_taken_seconds, 60)
        return f"{minutes}:{seconds:02d}"

    @property
    def percentage(self) -> int:
        if not self.total_questions:
            return 0
        return round((self.score / self.total_questions) * 100)

    def __str__(self):
        who = self.user or "Guest"
        return f"{who} - {self.category} - {self.score}/{self.total_questions}"


class Answer(models.Model):
    attempt = models.ForeignKey(TestAttempt, on_delete=models.CASCADE, related_name="answers")
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name="+")
    choice = models.ForeignKey(Choice, on_delete=models.SET_NULL, null=True, related_name="+")
    is_correct = models.BooleanField(default=False)


def _new_pass_token() -> str:
    return secrets.token_urlsafe(24)


class TestPass(models.Model):
    """
    A one-off paid pass for a single attempt at a paid test. No account is
    needed: whoever holds the secret token (in their private link, or in
    their browser session after paying) can take the test once and see the
    result afterwards.
    """

    STATUS_PENDING = "pending"
    STATUS_PAID = "paid"
    STATUS_FAILED = "failed"
    STATUS_CHOICES = [
        (STATUS_PENDING, "Pending"),
        (STATUS_PAID, "Paid"),
        (STATUS_FAILED, "Failed"),
    ]

    token = models.CharField(max_length=64, unique=True, default=_new_pass_token, editable=False)
    category = models.ForeignKey(Category, on_delete=models.PROTECT, related_name="passes")
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="test_passes",
        help_text="Set if the buyer happened to be logged in.",
    )
    email = models.EmailField(blank=True, help_text="Taken from Stripe Checkout once paid.")
    amount_cents = models.PositiveIntegerField()
    currency = models.CharField(max_length=3)
    stripe_checkout_session_id = models.CharField(max_length=255, blank=True, db_index=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default=STATUS_PENDING)
    created_at = models.DateTimeField(auto_now_add=True)
    paid_at = models.DateTimeField(null=True, blank=True)
    # Set the first time the test page is opened; the countdown runs from here
    # and can't be reset by refreshing, clearing cookies or switching devices.
    started_at = models.DateTimeField(null=True, blank=True)
    attempt = models.OneToOneField(
        TestAttempt, on_delete=models.SET_NULL, null=True, blank=True, related_name="test_pass"
    )

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.category} pass - {self.email or 'no email yet'} - {self.status}"

    def get_absolute_url(self):
        from django.urls import reverse

        return reverse("iqtest:pass_detail", kwargs={"token": self.token})

    @property
    def is_paid(self) -> bool:
        return self.status == self.STATUS_PAID

    @property
    def is_used(self) -> bool:
        return self.attempt_id is not None
