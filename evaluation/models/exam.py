from django.db import models
from django.core.validators import MinValueValidator

class Exam(models.Model):
    title = models.CharField(max_length=200)
    subject = models.CharField(max_length=100)
    instructions = models.TextField(blank=True)
    total_points = models.PositiveIntegerField(
        default=0,
        validators=[MinValueValidator(0)],
        help_text="Automatically calculated sum of all question points"
    )
    is_active = models.BooleanField(
        default=True,
        help_text="Whether the exam is currently active for submissions"
    )
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def update_total_points(self):
        """Recalculates and updates the total points based on related questions"""
        from django.db.models import Sum
        self.total_points = self.questions.aggregate(total=Sum('points'))['total'] or 0
        self.save()

    def __str__(self):
        return f"{self.title} ({self.subject})"

    class Meta:
        ordering = ['-created_at']