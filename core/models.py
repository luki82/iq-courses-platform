from django.db import models


class ContactMessage(models.Model):
    """A message sent through the Contact page. Read and reply from Django admin."""

    TOPIC_GENERAL = "general"
    TOPIC_CORRECTION = "correction"
    TOPIC_ADVERTISING = "advertising"
    TOPIC_OTHER = "other"
    TOPIC_CHOICES = [
        (TOPIC_GENERAL, "General question"),
        (TOPIC_CORRECTION, "Report a mistake in a lesson"),
        (TOPIC_ADVERTISING, "Advertising or sponsorship"),
        (TOPIC_OTHER, "Something else"),
    ]

    name = models.CharField(max_length=100)
    email = models.EmailField()
    topic = models.CharField(max_length=20, choices=TOPIC_CHOICES, default=TOPIC_GENERAL)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False, help_text="Tick once you've read or answered it.")

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.name} ({self.get_topic_display()}) - {self.created_at:%Y-%m-%d}"
