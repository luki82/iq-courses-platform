from django.shortcuts import render

from courses.models import Course
from iqtest.models import Category
from iqtest.views import FEATURED_SLUG


def home(request):
    # The headline timed IQ challenge (the Full IQ Assessment), if it's set up.
    challenge = Category.objects.filter(slug=FEATURED_SLUG).first()
    courses = Course.objects.filter(is_published=True).order_by("created_at")[:6]
    return render(request, "core/home.html", {"challenge": challenge, "courses": courses})
