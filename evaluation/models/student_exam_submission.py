from django.db import models
from evaluation.models import Exam, Student
from django.utils.translation import gettext_lazy as _
from django.core.validators import MinValueValidator, MaxValueValidator

class StatusChoice(models.TextChoices):
    PENDING = 'PENDING', _('Pending')
    SUBMITTED = 'SUBMITTED', _('Submitted')
    PROCESSING = 'PROCESSING', _('Processing')
    PARTIALLY_GRADED = 'PARTIALLY_GRADED', _('Partially Graded') # Added PARTIALLY_GRADED state for progressive grading
    GRADED = 'GRADED', _('Graded')
    ERROR = 'ERROR', _('Error')

class StudentExamSubmission(models.Model):
    exam = models.ForeignKey(
        Exam,
        on_delete=models.CASCADE,
        related_name='exam_submissions',
        verbose_name=_('Exam'),
        help_text="The exam being submitted"
    )
    
    student = models.ForeignKey(
        Student,
        on_delete=models.CASCADE,
        related_name='exam_submissions',
         help_text="Student for whom submitted the exam",
        verbose_name=_('Student')
    )

    
    answer_sheet = models.FileField(
        upload_to='exam_submissions/%Y/%m/%d/',
        verbose_name=_('Answer Sheet'),
        help_text=_('Upload scanned answer sheet in PDF format')
    )
    
    status = models.CharField(
        max_length=20,
        choices=StatusChoice.choices,
        default=StatusChoice.PENDING,
        verbose_name=_('Status'),
        db_index=True  # Better for filtering
    )
    
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name=_('Created At')
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name=_('Last Updated')
    )
    
    # Evaluation Results
    overall_score = models.FloatField(
        null=True,
        blank=True,
        help_text="Automatically calculated total score"
    )
    
    feedback = models.TextField(
        blank=True,
        verbose_name=_('Feedback'),
        help_text=_('Detailed feedback for the student')
    )
    
    # Additional useful fields
    processing_start_time = models.DateTimeField(
        null=True,
        blank=True,
        verbose_name=_('Processing Start Time')
    )
    
    processing_end_time = models.DateTimeField(
        null=True,
        blank=True,
        verbose_name=_('Processing End Time')
    )
    
    class Meta:
        unique_together = ('student', 'exam')
        verbose_name = _('Exam Submission')
        verbose_name_plural = _('Exam Submissions')
        ordering = ['-created_at']  # Newest first by default
        indexes = [
            models.Index(fields=['status']),
            models.Index(fields=['created_at']),
        ]
    
    def __str__(self):
        return _("{student}'s submission for {exam}").format(
            student=self.student.name,
            exam=self.exam.title
        )
    
    @property
    def processing_time(self):
        """Calculate total processing time if completed"""
        if self.processing_start_time and self.processing_end_time:
            return self.processing_end_time - self.processing_start_time
        return None