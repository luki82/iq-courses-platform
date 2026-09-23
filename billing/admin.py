from django.contrib import admin

from .models import Plan, Purchase


@admin.register(Plan)
class PlanAdmin(admin.ModelAdmin):
    list_display = ("name", "slug", "price_display", "duration_days", "is_active")
    prepopulated_fields = {"slug": ("name",)}


@admin.register(Purchase)
class PurchaseAdmin(admin.ModelAdmin):
    list_display = ("user", "plan", "status", "created_at", "completed_at")
    list_filter = ("status", "plan")
