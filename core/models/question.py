from django.db import models
from .exam import Exam

class Question(models.Model):
    exam = models.ForeignKey(Exam, related_name='questions', on_delete=models.CASCADE)
    text = models.TextField()
    ideal_answer = models.TextField()
    instructions = models.TextField(blank=True, null=True, help_text="Specific instructions for grading this question.")
    mark = models.PositiveIntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Question for {self.exam.title}"