from rest_framework import serializers
from ..models import Exam, Question
from .question import QuestionSerializer

class ExamSerializer(serializers.ModelSerializer):
    questions = QuestionSerializer(many=True)

    class Meta:
        model = Exam
        fields = ['id', 'title', 'subject', 'instructions', 'questions', 'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at']

    def create(self, validated_data):
        questions_data = validated_data.pop('questions')
        exam = Exam.objects.create(**validated_data)
        for question_data in questions_data:
            Question.objects.create(exam=exam, **question_data)
        return exam