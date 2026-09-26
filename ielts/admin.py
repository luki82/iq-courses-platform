from django.contrib import admin

from .models import IELTSLesson, IELTSQuestion


class IELTSQuestionInline(admin.TabularInline):
    model = IELTSQuestion
    extra = 0
    fields = ("order", "prompt", "question_type", "options", "correct_answer", "explanation")


@admin.register(IELTSLesson)
class IELTSLessonAdmin(admin.ModelAdmin):
    list_display = ("title", "tier", "skill", "diagram_type", "requires_premium", "created_at")
    list_filter = ("tier", "skill", "diagram_type")
    search_fields = ("title", "module_title", "passage_or_prompt")
    prepopulated_fields = {"slug": ("title",)}
    inlines = [IELTSQuestionInline]


@admin.register(IELTSQuestion)
class IELTSQuestionAdmin(admin.ModelAdmin):
    list_display = ("lesson", "order", "question_type", "correct_answer")
    list_filter = ("question_type",)
    search_fields = ("prompt", "explanation")
