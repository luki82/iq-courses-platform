import os

from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = (
        "Creates (or updates the password of) a superuser from the "
        "DJANGO_SUPERUSER_USERNAME / DJANGO_SUPERUSER_EMAIL / "
        "DJANGO_SUPERUSER_PASSWORD environment variables. Safe to run on "
        "every deploy -- does nothing if those env vars aren't set, and "
        "won't touch an existing account's password unless you also set "
        "DJANGO_SUPERUSER_RESET_PASSWORD=1."
    )

    def handle(self, *args, **options):
        username = os.environ.get("DJANGO_SUPERUSER_USERNAME")
        email = os.environ.get("DJANGO_SUPERUSER_EMAIL", "")
        password = os.environ.get("DJANGO_SUPERUSER_PASSWORD")
        reset_password = os.environ.get("DJANGO_SUPERUSER_RESET_PASSWORD") == "1"

        if not username or not password:
            self.stdout.write(
                "DJANGO_SUPERUSER_USERNAME / DJANGO_SUPERUSER_PASSWORD not "
                "set -- skipping admin creation."
            )
            return

        User = get_user_model()
        user, created = User.objects.get_or_create(
            username=username,
            defaults={"email": email, "is_staff": True, "is_superuser": True},
        )

        if created:
            user.set_password(password)
            user.is_staff = True
            user.is_superuser = True
            user.save()
            self.stdout.write(self.style.SUCCESS(f"Created superuser '{username}'."))
        elif reset_password:
            user.set_password(password)
            user.is_staff = True
            user.is_superuser = True
            user.save()
            self.stdout.write(
                self.style.SUCCESS(f"Updated password for existing user '{username}'.")
            )
        else:
            self.stdout.write(f"Superuser '{username}' already exists -- leaving as is.")