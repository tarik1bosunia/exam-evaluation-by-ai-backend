from django.db import models
from evaluation.models import Question, StudentExamSubmission

class Answer(models.Model):
    submission = models.ForeignKey(
        StudentExamSubmission,
        related_name='answers',
        on_delete=models.CASCADE
    )
    question = models.ForeignKey(
        Question,
        related_name='answers',
        on_delete=models.CASCADE
    )
    extracted_text = models.TextField(blank=True)
    image_path = models.CharField(max_length=255)
    score = models.FloatField(null=True, blank=True)
    feedback = models.TextField(blank=True)
    confidence = models.FloatField(null=True, blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('submission', 'question')
        
    def __str__(self):
        return f"Answer for Q{self.question.question_number} in {self.submission}"