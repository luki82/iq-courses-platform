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

    class Meta:
        verbose_name_plural = "categories"
        ordering = ["name"]

    def __str__(self):
        return self.name

    @property
    def question_count(self):
        return self.questions.count()


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
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="test_attempts")
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name="attempts")
    started_at = models.DateTimeField(auto_now_add=True)
    completed_at = models.DateTimeField(null=True, blank=True)
    score = models.PositiveIntegerField(default=0)
    total_questions = models.PositiveIntegerField(default=0)
    iq_score = models.PositiveIntegerField(null=True, blank=True)

    # Whether this particular attempt's full breakdown (explanations,
    # IQ score) is unlocked. Decided once, at submission time, from the
    # user's premium status / remaining free quota at that moment.
    detail_unlocked = models.BooleanField(default=False)

    class Meta:
        ordering = ["-started_at"]

    @property
    def percentage(self) -> int:
        if not self.total_questions:
            return 0
        return round((self.score / self.total_questions) * 100)

    def __str__(self):
        return f"{self.user} - {self.category} - {self.score}/{self.total_questions}"


class Answer(models.Model):
    attempt = models.ForeignKey(TestAttempt, on_delete=models.CASCADE, related_name="answers")
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name="+")
    choice = models.ForeignKey(Choice, on_delete=models.SET_NULL, null=True, related_name="+")
    is_correct = models.BooleanField(default=False)
