from django.apps import AppConfig


class AccountsConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "accounts"

    def ready(self):
        # Registers the post_save signal that creates a Profile for every new user.
        from . import signals  # noqa: F401
