import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="IELTSLesson",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("module_title", models.CharField(max_length=255)),
                (
                    "tier",
                    models.CharField(
                        choices=[
                            ("TIER_1", "Tier 1 -- Foundation (Band 4.5-5.5)"),
                            ("TIER_2", "Tier 2 -- Intermediate & Strategy (Band 6.0-6.5)"),
                            ("TIER_3", "Tier 3 -- Advanced Mastery (Band 7.0-9.0)"),
                        ],
                        max_length=10,
                    ),
                ),
                (
                    "skill",
                    models.CharField(
                        choices=[
                            ("READING", "Reading"),
                            ("LISTENING", "Listening"),
                            ("WRITING_T1", "Writing Task 1"),
                            ("WRITING_T2", "Writing Task 2"),
                            ("SPEAKING", "Speaking"),
                        ],
                        max_length=20,
                    ),
                ),
                ("title", models.CharField(help_text="The 'lesson_title' from the JSON module.", max_length=255)),
                ("slug", models.SlugField(blank=True, max_length=255, unique=True)),
                ("passage_or_prompt", models.TextField()),
                (
                    "diagram_type",
                    models.CharField(
                        choices=[
                            ("none", "None"),
                            ("chartjs", "Chart.js"),
                            ("mermaid", "Mermaid.js"),
                            ("cloudinary", "Cloudinary image"),
                        ],
                        default="none",
                        max_length=20,
                    ),
                ),
                ("diagram_config", models.JSONField(blank=True, default=dict)),
                ("band_9_sample", models.TextField(blank=True)),
                ("order", models.PositiveIntegerField(default=0)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
            ],
            options={
                "ordering": ["tier", "skill", "order", "id"],
            },
        ),
        migrations.CreateModel(
            name="IELTSQuestion",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                (
                    "order",
                    models.PositiveIntegerField(
                        default=0, help_text="Question number within the lesson (the JSON 'id')."
                    ),
                ),
                ("prompt", models.TextField()),
                (
                    "question_type",
                    models.CharField(
                        choices=[
                            ("multiple_choice", "Multiple choice"),
                            ("fill_blank", "Fill in the blank"),
                            ("true_false_ng", "True / False / Not Given"),
                        ],
                        max_length=20,
                    ),
                ),
                ("options", models.JSONField(blank=True, default=list)),
                ("correct_answer", models.CharField(max_length=500)),
                ("explanation", models.TextField()),
                (
                    "lesson",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="questions",
                        to="ielts.ieltslesson",
                    ),
                ),
            ],
            options={
                "ordering": ["order", "id"],
            },
        ),
    ]
