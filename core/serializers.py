from rest_framework import serializers
from .models import FileUpload

class FileUploadSerializer(serializers.ModelSerializer):
    class Meta:
        model = FileUpload
        fields = ['id', 'title', 'pdf_file', 'uploaded_at']
        read_only_fields = ['id', 'uploaded_at']
