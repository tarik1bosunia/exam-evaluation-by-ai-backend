from rest_framework import status
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser
from rest_framework.views import APIView
from ..models import StudentExamSubmission
# from evaluation.grading.workflows import 
from ..grading.workflows import grading_workflow

# Grading Views
class GradingView(APIView):
    parser_classes = [MultiPartParser]

    def post(self, request, pk):
        try:
            result = grading_workflow.invoke({
                "submission_id": str(pk),
                "page_images": [],
                "evaluations": []
            })
            # Ensure no PIL.Image objects remain in the response
            if "page_images" in result:
                del result["page_images"]  # Or convert them to base64
            return Response(result)
        except Exception as e:
            return Response({"error": str(e)}, status=400)

class StatusView(APIView):
    def get(self, request, pk):
        """Check grading status"""
        submission = StudentExamSubmission.objects.get(pk=pk)
        return Response({
            "status": submission.status,
            "score": submission.score,
            "feedback": submission.feedback
        })
        
        
        