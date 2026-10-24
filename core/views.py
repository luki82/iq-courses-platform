from django.http import HttpResponse
from django.shortcuts import render
from django.urls import reverse
from django.views.decorators.http import require_GET

from courses.models import Course
from iqtest.models import Category
from iqtest.views import FEATURED_SLUG


def home(request):
    # The headline timed IQ challenge (the Full IQ Assessment), if it's set up.
    challenge = Category.objects.filter(slug=FEATURED_SLUG).first()
    courses = Course.objects.filter(is_published=True).order_by("created_at")[:6]
    return render(request, "core/home.html", {"challenge": challenge, "courses": courses})


def about(request):
    return render(request, "core/about.html")


def privacy(request):
    return render(request, "core/privacy.html")


def contact(request):
    return render(request, "core/contact.html")


@require_GET
def robots_txt(request):
    sitemap_url = request.build_absolute_uri(reverse("django.contrib.sitemaps.views.sitemap"))
    lines = [
        "User-agent: *",
        "Disallow: /admin/",
        "Disallow: /accounts/",
        "Disallow: /billing/donate/checkout/",
        "Disallow: /iq-test/result/",
        "Disallow: /iq-test/pass/",
        "",
        f"Sitemap: {sitemap_url}",
    ]
    return HttpResponse("\n".join(lines) + "\n", content_type="text/plain")
