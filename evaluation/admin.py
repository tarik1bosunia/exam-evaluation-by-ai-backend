from django.contrib import admin
from django.urls import reverse
from django.utils.html import format_html
from django.utils.translation import gettext_lazy as _
from .models import Exam, Question, Student, StudentExamSubmission

class QuestionInline(admin.TabularInline):
    model = Question
    extra = 1
    fields = ('text', 'points', 'ideal_answer', 'created_at')
    readonly_fields = ('created_at',)
    ordering = ('created_at',)
    show_change_link = True

@admin.register(Exam)
class ExamAdmin(admin.ModelAdmin):
    list_display = ('title', 'subject', 'question_count', 'total_points', 'created_at')
    list_filter = ('subject', 'created_at')
    search_fields = ('title', 'subject', 'instructions')
    list_select_related = True
    readonly_fields = ('total_points', 'created_at', 'updated_at')
    fieldsets = (
        (None, {
            'fields': ('title', 'subject', 'instructions')
        }),
        ('Statistics', {
            'fields': ('total_points', 'created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    inlines = [QuestionInline]
    
    def get_queryset(self, request):
        return super().get_queryset(request).prefetch_related('questions')
    
    def question_count(self, obj):
        count = obj.questions.count()
        url = reverse('admin:evaluation_question_changelist') + f'?exam__id__exact={obj.id}'
        return format_html('<a href="{}">{} Questions</a>', url, count)
    question_count.short_description = _('Questions')

@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ('truncated_text', 'exam_link', 'points', 'ideal_answer_preview', 'created_at')
    list_filter = ('exam__title', 'points', 'created_at')
    search_fields = ('text', 'ideal_answer', 'exam__title')
    list_select_related = ('exam',)
    readonly_fields = ('created_at', 'updated_at')
    list_per_page = 30
    
    def exam_link(self, obj):
        url = reverse('admin:evaluation_exam_change', args=[obj.exam.id])
        return format_html('<a href="{}">{}</a>', url, obj.exam.title)
    exam_link.short_description = _('Exam')
    exam_link.admin_order_field = 'exam__title'
    
    def truncated_text(self, obj):
        return obj.text[:100] + '...' if len(obj.text) > 100 else obj.text
    truncated_text.short_description = _('Question Text')
    
    def ideal_answer_preview(self, obj):
        return obj.ideal_answer[:100] + '...' if len(obj.ideal_answer) > 100 else obj.ideal_answer
    ideal_answer_preview.short_description = _('Ideal Answer Preview')

@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ('student_id', 'name', 'email', 'academic_info', 'submission_count', 'created_at')
    list_filter = ('department', 'semester', 'created_at')
    search_fields = ('student_id', 'name', 'email', 'department')
    list_select_related = True
    readonly_fields = ('created_at', 'updated_at', 'submission_links')
    fieldsets = (
        (_('Basic Information'), {
            'fields': ('student_id', 'name', 'email')
        }),
        (_('Academic Information'), {
            'fields': ('department', 'semester'),
            'classes': ('collapse',)
        }),
        (_('Metadata'), {
            'fields': ('created_at', 'updated_at', 'submission_links'),
            'classes': ('collapse',)
        }),
    )
    
    def academic_info(self, obj):
        info = []
        if obj.department:
            info.append(obj.department)
        if obj.semester:
            info.append(f"Sem {obj.semester}")
        return ' | '.join(info) if info else '-'
    academic_info.short_description = _('Academic Info')
    
    def submission_count(self, obj):
        count = obj.submissions.count()
        url = reverse('admin:evaluation_studentexamsubmission_changelist') + f'?student__id__exact={obj.id}'
        return format_html('<a href="{}">{} {}</a>', url, count, _('submissions'))
    submission_count.short_description = _('Submissions')
    
    def submission_links(self, obj):
        submissions = obj.submissions.select_related('exam').order_by('-created_at')[:5]
        links = []
        for sub in submissions:
            url = reverse('admin:evaluation_studentexamsubmission_change', args=[sub.id])
            links.append(f'<li><a href="{url}">{sub.exam.title} ({sub.get_status_display()})</a></li>')
        return format_html('<ul>{}</ul>', ''.join(links)) if links else _('No submissions yet')
    submission_links.short_description = _('Recent Submissions')

@admin.register(StudentExamSubmission)
class StudentExamSubmissionAdmin(admin.ModelAdmin):
    list_display = ('id', 'student_exam', 'status_badge', 'score_display', 'processing_time', 'created_at')
    list_filter = ('status', 'exam', 'created_at')
    search_fields = ('student__name', 'student__student_id', 'exam__title')
    list_select_related = ('student', 'exam')
    readonly_fields = ('created_at', 'updated_at', 'processing_time', 'answer_sheet_link', 'feedback_preview')
    raw_id_fields = ('student', 'exam')
    date_hierarchy = 'created_at'
    actions = ['mark_as_graded', 'mark_as_processing']
    list_per_page = 30
    
    fieldsets = (
        (_('Submission Info'), {
            'fields': ('student', 'exam')
        }),
        (_('Status & Evaluation'), {
            'fields': ('status', 'score', 'feedback', 'feedback_preview')
        }),
        (_('Answer Sheet'), {
            'fields': ('answer_sheet_link', 'answer_sheet')
        }),
        (_('Processing Info'), {
            'fields': ('processing_start_time', 'processing_end_time', 'processing_time'),
            'classes': ('collapse',)
        }),
        (_('Metadata'), {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    def student_exam(self, obj):
        student_url = reverse('admin:evaluation_student_change', args=[obj.student.id])
        exam_url = reverse('admin:evaluation_exam_change', args=[obj.exam.id])
        return format_html(
            '<a href="{}">{}</a> - <a href="{}">{}</a>',
            exam_url, obj.exam.title,
            student_url, obj.student.name
        )
    student_exam.short_description = _('Exam | Student')
    student_exam.admin_order_field = 'exam__title'
    
    def status_badge(self, obj):
        colors = {
            'PENDING': 'gray',
            'SUBMITTED': 'blue',
            'PROCESSING': 'orange',
            'PARTIALLY_GRADED': 'yellow',
            'GRADED': 'green',
            'ERROR': 'red'
        }
        return format_html(
            '<span style="background:{}; color:white; padding:2px 6px; border-radius:10px">{}</span>',
            colors.get(obj.status, 'gray'),
            obj.get_status_display()
        )
    status_badge.short_description = _('Status')
    
    def score_display(self, obj):
        if obj.score is not None:
            return f"{obj.score:.1f}/100"
        return "-"
    score_display.short_description = _('Score')
    
    def answer_sheet_link(self, obj):
        if obj.answer_sheet:
            return format_html(
                '<a href="{}" target="_blank" class="button">{}</a>',
                obj.answer_sheet.url,
                _('View Answer Sheet')
            )
        return "-"
    answer_sheet_link.short_description = _('Answer Sheet')
    
    def feedback_preview(self, obj):
        return obj.feedback[:200] + '...' if obj.feedback and len(obj.feedback) > 200 else obj.feedback or "-"
    feedback_preview.short_description = _('Feedback Preview')
    
    def mark_as_graded(self, request, queryset):
        updated = queryset.update(status='GRADED')
        self.message_user(request, _('Successfully marked %(count)d submissions as graded') % {'count': updated})
    mark_as_graded.short_description = _('Mark selected as GRADED')
    
    def mark_as_processing(self, request, queryset):
        updated = queryset.update(status='PROCESSING')
        self.message_user(request, _('Successfully marked %(count)d submissions as PROCESSING') % {'count': updated})
    mark_as_processing.short_description = _('Mark selected as PROCESSING')
    
    def processing_time(self, obj):
        if obj.processing_start_time and obj.processing_end_time:
            duration = obj.processing_end_time - obj.processing_start_time
            return f"{duration.total_seconds():.1f} {_('seconds')}"
        return "-"
    processing_time.short_description = _('Processing Time')

# Admin site customization
admin.site.site_header = _('Exam Evaluation System Administration')
admin.site.site_title = _('Exam Evaluation System')
admin.site.index_title = _('Dashboard')