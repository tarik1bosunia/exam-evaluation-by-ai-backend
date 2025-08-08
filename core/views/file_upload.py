
from rest_framework import generics
from ..models import FileUpload
from ..serializers import FileUploadSerializer

class FileUploadView(generics.CreateAPIView):
    queryset = FileUpload.objects.all()
    serializer_class = FileUploadSerializer
