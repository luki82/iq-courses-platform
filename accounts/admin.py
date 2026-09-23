from django.contrib import admin

from .models import Profile


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ("user", "is_premium", "premium_until", "free_test_attempts_used")
    list_filter = ("is_premium",)
    search_fields = ("user__username", "user__email")
