from django.db import models
from django.utils.text import slugify


class IELTSLesson(models.Model):
    """
    One IELTS lesson module -- matches the JSON schema used to generate
    lesson content (module_title, tier, skill, lesson_title, passage_or_prompt,
    diagram_type, diagram_config, questions, band_9_sample).

    Freemium rule: TIER_1 lessons are always free; TIER_2 and TIER_3 require
    request.user.profile.has_premium_access, same as Premium categories in
    the iqtest app and Premium modules in the courses app (see requires_premium).
    """

    TIER_CHOICES = [
        ("TIER_1", "Tier 1 -- Foundation (Band 4.5-5.5)"),
        ("TIER_2", "Tier 2 -- Intermediate & Strategy (Band 6.0-6.5)"),
        ("TIER_3", "Tier 3 -- Advanced Mastery (Band 7.0-9.0)"),
    ]
    SKILL_CHOICES = [
        ("READING", "Reading"),
        ("LISTENING", "Listening"),
        ("WRITING_T1", "Writing Task 1"),
        ("WRITING_T2", "Writing Task 2"),
        ("SPEAKING", "Speaking"),
    ]
    DIAGRAM_CHOICES = [
        ("none", "None"),
        ("chartjs", "Chart.js"),
        ("mermaid", "Mermaid.js"),
        ("cloudinary", "Cloudinary image"),
    ]

    module_title = models.CharField(max_length=255)
    tier = models.CharField(max_length=10, choices=TIER_CHOICES)
    skill = models.CharField(max_length=20, choices=SKILL_CHOICES)
    title = models.CharField(max_length=255, help_text="The 'lesson_title' from the JSON module.")
    slug = models.SlugField(max_length=255, unique=True, blank=True)
    passage_or_prompt = models.TextField()
    diagram_type = models.CharField(max_length=20, choices=DIAGRAM_CHOICES, default="none")
    diagram_config = models.JSONField(default=dict, blank=True)
    band_9_sample = models.TextField(blank=True)
    order = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["tier", "skill", "order", "id"]

    def save(self, *args, **kwargs):
        if not self.slug:
            base = slugify(self.title)[:240] or "lesson"
            slug = base
            i = 1
            while IELTSLesson.objects.filter(slug=slug).exclude(pk=self.pk).exists():
                i += 1
                slug = f"{base}-{i}"
            self.slug = slug
        super().save(*args, **kwargs)

    def __str__(self):
        return f"[{self.tier}] {self.title}"

    @property
    def requires_premium(self) -> bool:
        """Tier 1 is always free; Tier 2 and Tier 3 sit behind Premium."""
        return self.tier != "TIER_1"


class IELTSQuestion(models.Model):
    QUESTION_TYPE_CHOICES = [
        ("multiple_choice", "Multiple choice"),
        ("fill_blank", "Fill in the blank"),
        ("true_false_ng", "True / False / Not Given"),
    ]

    lesson = models.ForeignKey(IELTSLesson, on_delete=models.CASCADE, related_name="questions")
    order = models.PositiveIntegerField(
        default=0, help_text="Question number within the lesson (the JSON 'id')."
    )
    prompt = models.TextField()
    question_type = models.CharField(max_length=20, choices=QUESTION_TYPE_CHOICES)
    options = models.JSONField(default=list, blank=True)
    correct_answer = models.CharField(max_length=500)
    explanation = models.TextField()

    class Meta:
        ordering = ["order", "id"]

    def __str__(self):
        return f"Q{self.order}: {self.prompt[:60]}"
