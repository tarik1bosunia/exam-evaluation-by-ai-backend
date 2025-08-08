from django.db import models

class Student(models.Model):
    # Basic Information
    student_id = models.CharField(max_length=20, unique=True)
    name = models.CharField(max_length=100)
    email = models.EmailField(blank=True, null=True)
    
    # Academic Information
    department = models.CharField(max_length=100, blank=True, null=True)
    semester = models.PositiveIntegerField(blank=True, null=True)
    
    # Metadata
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.name} ({self.student_id})"

