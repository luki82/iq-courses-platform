"""
Create the default Premium plans.

Run with:  python manage.py seed_plans

Runs on every deploy (see build.sh) but only CREATES plans that don't exist
yet -- once a plan is in the database, edit its price, duration or wording in
Django admin and redeploys won't overwrite your changes. Pass --reset to force
these defaults back onto existing plans.
"""
from django.core.management.base import BaseCommand

from billing.models import Plan

PLANS = [
    {
        "slug": "premium-30",
        "name": "1 Month",
        "description": "Try everything for a month.",
        "price_display": "A$14.99",
        "price_cents": 1499,
        "duration_days": 30,
    },
    {
        "slug": "premium-90",
        "name": "3 Months",
        "description": "The usual time to prepare for an IELTS test.",
        "price_display": "A$34.99",
        "price_cents": 3499,
        "duration_days": 90,
    },
    {
        "slug": "premium-365",
        "name": "12 Months",
        "description": "Best value -- a full year of learning.",
        "price_display": "A$99",
        "price_cents": 9900,
        "duration_days": 365,
    },
]


class Command(BaseCommand):
    help = "Creates the default Premium plans (AUD) if they don't already exist."

    def add_arguments(self, parser):
        parser.add_argument("--reset", action="store_true", help="Overwrite existing plans with these defaults.")

    def handle(self, *args, **options):
        created_count = 0
        for data in PLANS:
            defaults = {k: v for k, v in data.items() if k != "slug"} | {"currency": "aud", "is_active": True}
            if options["reset"]:
                _, created = Plan.objects.update_or_create(slug=data["slug"], defaults=defaults)
            else:
                _, created = Plan.objects.get_or_create(slug=data["slug"], defaults=defaults)
            created_count += created
        self.stdout.write(
            self.style.SUCCESS(f"Plans ready: {created_count} created, {len(PLANS) - created_count} already existed.")
        )
