from django.contrib import admin

from .models import Answer, Category, Choice, Question, TestAttempt


class ChoiceInline(admin.TabularInline):
    model = Choice
    extra = 4


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("name", "slug", "is_premium", "question_count")
    prepopulated_fields = {"slug": ("name",)}


@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ("text", "category", "order")
    list_filter = ("category",)
    inlines = [ChoiceInline]


@admin.register(TestAttempt)
class TestAttemptAdmin(admin.ModelAdmin):
    list_display = ("user", "category", "score", "total_questions", "iq_score", "detail_unlocked", "started_at")
    list_filter = ("category", "detail_unlocked")


admin.site.register(Answer)
