from django.shortcuts import render

from courses.models import Course
from iqtest.models import Category


def home(request):
    categories = Category.objects.all()[:4]
    courses = Course.objects.filter(is_published=True)[:4]
    return render(
        request,
        "core/home.html",
        {"categories": categories, "courses": courses},
    )
