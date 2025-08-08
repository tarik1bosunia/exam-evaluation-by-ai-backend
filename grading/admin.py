from django.contrib import admin
from .models import GradingJob

@admin.register(GradingJob)
class GradingJobAdmin(admin.ModelAdmin):
    list_display = ("id", "question", "max_points", "created_at")
    readonly_fields = ("ocr_output", "evaluation_result", "created_at", "updated_at")
    search_fields = ("question", "ideal_answer")
    list_filter = ("created_at",)
