from rest_framework import serializers
from .models import GradingJob

class GradingJobSerializer(serializers.ModelSerializer):
    class Meta:
        model = GradingJob
        fields = '__all__'
        read_only_fields = ['ocr_output', 'evaluation_result', 'created_at', 'updated_at']
