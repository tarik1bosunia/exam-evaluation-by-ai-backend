from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from evaluation.models import StudentExamSubmission
from evaluation.serializers.submission import SubmissionSerializer
from evaluation.tasks import grade_submission_task

class SubmissionViewSet(viewsets.ModelViewSet):
    queryset = StudentExamSubmission.objects.all()
    serializer_class = SubmissionSerializer
    
    @action(detail=True, methods=['post'])
    def grade(self, request, pk=None):
        submission = self.get_object()
        
        if submission.status not in ['PENDING', 'SUBMITTED']:
            return Response(
                {'error': 'Submission is already being processed or graded'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        grade_submission_task.delay(submission.id)
        
        submission.refresh_from_db()
        return Response(
            self.get_serializer(submission).data,
            status=status.HTTP_202_ACCEPTED
        )
    
    @action(detail=True, methods=['get'])
    def answers(self, request, pk=None):
        submission = self.get_object()
        answers = submission.answers.all()
        serializer = AnswerSerializer(answers, many=True)
        return Response(serializer.data)