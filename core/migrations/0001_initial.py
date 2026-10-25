from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="ContactMessage",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("name", models.CharField(max_length=100)),
                ("email", models.EmailField(max_length=254)),
                (
                    "topic",
                    models.CharField(
                        choices=[
                            ("general", "General question"),
                            ("correction", "Report a mistake in a lesson"),
                            ("advertising", "Advertising or sponsorship"),
                            ("other", "Something else"),
                        ],
                        default="general",
                        max_length=20,
                    ),
                ),
                ("message", models.TextField()),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("is_read", models.BooleanField(default=False, help_text="Tick once you've read or answered it.")),
            ],
            options={
                "ordering": ["-created_at"],
            },
        ),
    ]
