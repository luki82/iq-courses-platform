from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render

from courses.models import Enrollment
from iqtest.models import TestAttempt

from .forms import SignUpForm


def signup(request):
    if request.user.is_authenticated:
        return redirect("core:home")

    if request.method == "POST":
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect("core:home")
    else:
        form = SignUpForm()
    return render(request, "accounts/signup.html", {"form": form})


@login_required
def profile(request):
    attempts = TestAttempt.objects.filter(user=request.user).select_related("category")[:10]
    enrollments = Enrollment.objects.filter(user=request.user).select_related("course")
    return render(
        request,
        "accounts/profile.html",
        {
            "profile": request.user.profile,
            "attempts": attempts,
            "enrollments": enrollments,
        },
    )
