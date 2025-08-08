# grading/views/grading_job_view.py

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import GradingJobSerializer
from grading.services.grading_executor import execute_grading_job


class GradingJobView(APIView):
    def post(self, request):
        try:
            job = execute_grading_job(
                image_path=r"D:\test florence 2 model\images\page1.jpeg",
                question="What is the capital of Bangladesh?",
                ideal_answer="The capital of Bangladesh is Dhaka.",
                max_points=5,
                grading_criteria="""
                - Correct capital name: 3 points
                - Complete sentence structure: 2 points
                - Spelling/grammar: 1 point (bonus)
                """
            )

            return Response(GradingJobSerializer(job).data, status=status.HTTP_200_OK)

        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
