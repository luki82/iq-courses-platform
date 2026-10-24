from django.urls import path

from . import views

app_name = "billing"

urlpatterns = [
    path("donate/", views.donate, name="donate"),
    path("donate/checkout/", views.donate_checkout, name="donate_checkout"),
    path("donate/thanks/", views.donate_thanks, name="donate_thanks"),
    # Old Premium page: redirects to Donate so existing links keep working.
    path("pricing/", views.pricing, name="pricing"),
    path("webhook/", views.stripe_webhook, name="stripe_webhook"),
]
