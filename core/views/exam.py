from rest_framework import generics
from ..models import Exam
from ..serializers import ExamSerializer

class ExamCreateView(generics.CreateAPIView):
    queryset = Exam.objects.all()
    serializer_class = ExamSerializer

class ExamListView(generics.ListAPIView):
    queryset = Exam.objects.all().order_by('-created_at') # Show newest first
    serializer_class = ExamSerializer
    

class ExamDetailView(generics.RetrieveAPIView):
    queryset = Exam.objects.all()
    serializer_class = ExamSerializer
    lookup_field = 'pk'   