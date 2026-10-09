from django.contrib import admin

from .models import Answer, Category, Choice, Question, TestAttempt, TestPass


class ChoiceInline(admin.TabularInline):
    model = Choice
    extra = 4


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("name", "slug", "is_premium", "price_cents", "time_limit_minutes", "question_count")
    prepopulated_fields = {"slug": ("name",)}


@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ("text", "category", "order")
    list_filter = ("category",)
    inlines = [ChoiceInline]


@admin.register(TestAttempt)
class TestAttemptAdmin(admin.ModelAdmin):
    list_display = ("user", "category", "score", "total_questions", "iq_score", "time_taken_seconds", "detail_unlocked", "started_at")
    list_filter = ("category", "detail_unlocked")


@admin.register(TestPass)
class TestPassAdmin(admin.ModelAdmin):
    list_display = ("category", "email", "user", "status", "amount_cents", "currency", "paid_at", "started_at", "attempt")
    list_filter = ("status", "category")
    search_fields = ("email", "stripe_checkout_session_id", "token")
    readonly_fields = ("token", "stripe_checkout_session_id", "created_at", "paid_at", "started_at", "attempt")


admin.site.register(Answer)
