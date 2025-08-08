from rest_framework import generics, status, filters
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser, FormParser
from django_filters.rest_framework import DjangoFilterBackend
from ..models import Exam, Question, Student, StudentExamSubmission
from ..serializers import (
    ExamSerializer, QuestionSerializer,
    StudentSerializer, StudentExamSubmissionSerializer,
    SubmissionCreateSerializer
)

class ExamListCreateView(generics.ListCreateAPIView):
    queryset = Exam.objects.all().prefetch_related('questions')
    serializer_class = ExamSerializer
    filter_backends = [filters.SearchFilter, DjangoFilterBackend]
    search_fields = ['title', 'subject']
    filterset_fields = ['subject']

class ExamDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Exam.objects.all().prefetch_related('questions')
    serializer_class = ExamSerializer

class QuestionListCreateView(generics.ListCreateAPIView):
    serializer_class = QuestionSerializer
    
    def get_queryset(self):
        exam_id = self.kwargs.get('exam_id')
        return Question.objects.filter(exam_id=exam_id)
    
    def perform_create(self, serializer):
        exam_id = self.kwargs.get('exam_id')
        serializer.save(exam_id=exam_id)

class QuestionDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = QuestionSerializer
    
    def get_queryset(self):
        exam_id = self.kwargs.get('exam_id')
        return Question.objects.filter(exam_id=exam_id)

class StudentListCreateView(generics.ListCreateAPIView):
    queryset = Student.objects.all()
    serializer_class = StudentSerializer
    filter_backends = [filters.SearchFilter, DjangoFilterBackend]
    search_fields = ['name', 'student_id', 'email']
    filterset_fields = ['department', 'semester']

class StudentDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Student.objects.all()
    serializer_class = StudentSerializer

class SubmissionListCreateView(generics.ListCreateAPIView):
    queryset = StudentExamSubmission.objects.all().select_related('student', 'exam')
    parser_classes = [MultiPartParser, FormParser]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['student', 'exam', 'status']
    
    def get_serializer_class(self):
        if self.request.method == 'POST':
            return SubmissionCreateSerializer
        return StudentExamSubmissionSerializer
    
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        submission = serializer.save(status='SUBMITTED')
        
        # Prepare response with full submission details
        response_serializer = StudentExamSubmissionSerializer(submission)
        headers = self.get_success_headers(response_serializer.data)
        return Response(
            response_serializer.data,
            status=status.HTTP_201_CREATED,
            headers=headers
        )

class SubmissionDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = StudentExamSubmission.objects.all().select_related('student', 'exam')
    serializer_class = StudentExamSubmissionSerializer
    
    def get_parser_classes(self):
        if self.request.method in ['PUT', 'PATCH']:
            return [MultiPartParser, FormParser]
        return super().get_parser_classes()

class ExamSubmissionsView(generics.ListAPIView):
    serializer_class = StudentExamSubmissionSerializer
    
    def get_queryset(self):
        exam_id = self.kwargs.get('exam_id')
        return StudentExamSubmission.objects.filter(exam_id=exam_id).select_related('student')

class StudentSubmissionsView(generics.ListAPIView):
    serializer_class = StudentExamSubmissionSerializer
    
    def get_queryset(self):
        student_id = self.kwargs.get('student_id')
        return StudentExamSubmission.objects.filter(student_id=student_id).select_related('exam')