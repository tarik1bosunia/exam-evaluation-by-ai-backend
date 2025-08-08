from django.db import models

class GradingJob(models.Model):
    image = models.ImageField(upload_to='grading_images/')
    question = models.TextField()
    ideal_answer = models.TextField()
    criteria = models.TextField()
    max_points = models.IntegerField()

    ocr_output = models.JSONField(null=True, blank=True)
    evaluation_result = models.JSONField(null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Grading Job #{self.id}"
