from django.contrib import admin
from .models import FileUpload, Exam, Question

class QuestionInline(admin.TabularInline):
    model = Question
    extra = 1  # Number of extra forms to display

@admin.register(Exam)
class ExamAdmin(admin.ModelAdmin):
    list_display = ('title', 'subject', 'created_at', 'updated_at')
    search_fields = ('title', 'subject')
    list_filter = ('created_at', 'updated_at')
    inlines = [QuestionInline]

@admin.register(FileUpload)
class FileUploadAdmin(admin.ModelAdmin):
    list_display = ('title', 'pdf_file', 'uploaded_at')
    search_fields = ('title',)
    list_filter = ('uploaded_at',)

@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ('text', 'exam', 'mark', 'created_at')
    search_fields = ('text', 'exam__title')
    list_filter = ('created_at', 'exam')
