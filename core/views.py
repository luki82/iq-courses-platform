import time

from django.conf import settings
from django.contrib import messages
from django.http import Http404, HttpResponse
from django.shortcuts import redirect, render
from django.urls import reverse
from django.views.decorators.http import require_GET

from courses.models import Course
from iqtest.models import Category
from iqtest.views import FEATURED_SLUG

from .forms import ContactForm

# Each browser can send at most this many contact messages per hour.
CONTACT_LIMIT = 3
CONTACT_WINDOW_SECONDS = 60 * 60


def home(request):
    # The headline timed IQ challenge (the Full IQ Assessment), if it's set up.
    challenge = Category.objects.filter(slug=FEATURED_SLUG).first()
    courses = Course.objects.filter(is_published=True).order_by("created_at")[:6]
    return render(request, "core/home.html", {"challenge": challenge, "courses": courses})


def about(request):
    return render(request, "core/about.html")


def privacy(request):
    return render(request, "core/privacy.html")


def terms(request):
    return render(request, "core/terms.html")


def contact(request):
    if request.method == "POST":
        form = ContactForm(request.POST)
        now = time.time()
        recent = [t for t in request.session.get("contact_sent", []) if now - t < CONTACT_WINDOW_SECONDS]
        if len(recent) >= CONTACT_LIMIT:
            messages.error(request, "You've sent several messages recently. Please try again in an hour.")
            return redirect("core:contact")
        if form.is_valid():
            if not form.is_spam():
                form.save()
                request.session["contact_sent"] = recent + [now]
            messages.success(request, "Thanks for your message! We usually reply within a few days.")
            return redirect("core:contact")
    else:
        form = ContactForm()
    return render(request, "core/contact.html", {"form": form})


@require_GET
def ads_txt(request):
    """
    Google AdSense asks every site to publish /ads.txt listing who may sell its
    ad space. It is filled in from ADSENSE_CLIENT_ID (e.g. ca-pub-1234567890123456).
    """
    client = settings.ADSENSE_CLIENT_ID
    if not client:
        raise Http404("AdSense is not set up yet.")
    publisher = client.removeprefix("ca-")
    return HttpResponse(f"google.com, {publisher}, DIRECT, f08c47fec0942fa0\n", content_type="text/plain")


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
