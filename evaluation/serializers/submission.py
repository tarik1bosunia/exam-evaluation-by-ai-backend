from rest_framework import serializers
from evaluation.models import StudentExamSubmission

class SubmissionSerializer(serializers.ModelSerializer):
    class Meta:
        model = StudentExamSubmission
        fields = '__all__'
        read_only_fields = (
            'status', 'score', 'feedback', 
            'created_at', 'updated_at',
            'processing_start_time', 'processing_end_time'
        )