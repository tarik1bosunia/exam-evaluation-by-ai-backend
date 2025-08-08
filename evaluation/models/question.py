from django.db import models
from django.core.validators import MinValueValidator
from .exam import Exam

class Question(models.Model):
    exam = models.ForeignKey(
        Exam,
        related_name='questions',
        on_delete=models.CASCADE,
        help_text="The exam this question belongs to"
    )
    text = models.TextField(help_text="The question text.")
    points = models.PositiveIntegerField(
        help_text="Points awarded for this question.",
        validators=[MinValueValidator(1)]
    )
    ideal_answer = models.TextField(help_text="Model answer for scoring reference")
    
    question_number = models.CharField(
        max_length=20,
        help_text="Question identifier (e.g., '1', '2a', '3b')"
    )
    
    grading_criteria = models.TextField( # TODO: in future need to convert it as a model
        blank=True,
        null=True,
        help_text="Grading criteria and rubric (markdown supported)"
    )
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        is_new = self._state.adding  # Check if this is a new question
        super().save(*args, **kwargs)
        if is_new or 'points' in kwargs.get('update_fields', []):
            self.exam.update_total_points()
            
    def delete(self, *args, **kwargs):
        exam = self.exam
        super().delete(*args, **kwargs)
        exam.update_total_points()
        
    class Meta:
        ordering = ['question_number']
        unique_together = ('exam', 'question_number')
        verbose_name = 'Question'
        verbose_name_plural = 'Questions'    

    def __str__(self):
        return f"Q{self.question_number} - {self.points} points: {self.text[:50]}..."