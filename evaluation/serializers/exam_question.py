from rest_framework import serializers
from ..models import Exam, Question, Student, StudentExamSubmission

class QuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Question
        fields = ['id', 'text', 'points', 'ideal_answer', 'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at']

class ExamSerializer(serializers.ModelSerializer):
    questions = QuestionSerializer(many=True, read_only=True)
    
    class Meta:
        model = Exam
        fields = ['id', 'title', 'subject', 'instructions', 
                 'created_at', 'updated_at', 'total_points', 'questions']
        read_only_fields = ['id', 'created_at', 'updated_at', 'total_points', 'questions']


class StudentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Student
        fields = ['id', 'student_id', 'name', 'email', 
                'department', 'semester', 'created_at']
        read_only_fields = ['id', 'created_at']

class StudentExamSubmissionSerializer(serializers.ModelSerializer):
    student = StudentSerializer(read_only=True)
    exam = ExamSerializer(read_only=True)
    answer_sheet_url = serializers.SerializerMethodField()
    processing_time = serializers.SerializerMethodField()
    
    class Meta:
        model = StudentExamSubmission
        fields = ['id', 'student', 'exam', 'status', 'score', 
                'feedback', 'answer_sheet', 'answer_sheet_url',
                'processing_start_time', 'processing_end_time',
                'processing_time', 'created_at']
        read_only_fields = ['id', 'created_at', 'processing_time']
        extra_kwargs = {
            'answer_sheet': {'write_only': True}
        }
    
    def get_answer_sheet_url(self, obj):
        if obj.answer_sheet:
            return obj.answer_sheet.url
        return None
    
    def get_processing_time(self, obj):
        if obj.processing_start_time and obj.processing_end_time:
            return (obj.processing_end_time - obj.processing_start_time).total_seconds()
        return None

class SubmissionCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = StudentExamSubmission
        fields = ['exam', 'student', 'answer_sheet']
    
    def validate_answer_sheet(self, value):
        if not value.name.endswith('.pdf'):
            raise serializers.ValidationError(_("Only PDF files are allowed"))
        if value.size > 50 * 1024 * 1024:  # 50MB limit
            raise serializers.ValidationError(_("File size exceeds 50MB limit"))
        return value