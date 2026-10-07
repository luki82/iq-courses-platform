from django.urls import path

from . import views

app_name = "billing"

# Order matters: the fixed checkout/success/ and checkout/cancel/ routes must
# come before checkout/<slug>/, or "success" would be treated as a plan slug.
urlpatterns = [
    path("pricing/", views.pricing, name="pricing"),
    path("checkout/success/", views.checkout_success, name="checkout_success"),
    path("checkout/cancel/", views.checkout_cancel, name="checkout_cancel"),
    path("checkout/<slug:slug>/", views.create_checkout_session, name="create_checkout_session"),
    path("webhook/", views.stripe_webhook, name="stripe_webhook"),
]
