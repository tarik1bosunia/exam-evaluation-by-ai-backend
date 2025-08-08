from rest_framework import generics
from ..models import Exam
from ..serializers import ExamSerializer

class ExamCreateView(generics.CreateAPIView):
    queryset = Exam.objects.all()
    serializer_class = ExamSerializer