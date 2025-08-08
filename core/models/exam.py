from django.db import models

class Exam(models.Model):
    title = models.CharField(max_length=255)
    subject = models.CharField(max_length=255)
    instructions = models.TextField(help_text="Instructions for the AI on how to grade the exam.")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title
