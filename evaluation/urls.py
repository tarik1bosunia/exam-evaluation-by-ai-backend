from django.urls import path
from .views import (
    ExamListCreateView, ExamDetailView,
    QuestionListCreateView, StudentListCreateView,
    SubmissionListCreateView, SubmissionDetailView,
    ExamSubmissionsView, StudentSubmissionsView,
    GradingView, StatusView
)

urlpatterns = [
    path('exams/', ExamListCreateView.as_view()),
    path('exams/<int:pk>/', ExamDetailView.as_view()),
    
    path('exams/<int:exam_id>/questions/', QuestionListCreateView.as_view()),
    path('exams/<int:exam_id>/submissions/', ExamSubmissionsView.as_view()),
    
    path('students/', StudentListCreateView.as_view()),
    path('students/<int:student_id>/submissions/', StudentSubmissionsView.as_view()),
    
    path('submissions/', SubmissionListCreateView.as_view()),
    path('submissions/<int:pk>/', SubmissionDetailView.as_view()),
    
        # Grading endpoints
    path('submissions/<int:pk>/grade/', GradingView.as_view(), name='grade-submission'),
    path('submissions/<int:pk>/status/', StatusView.as_view(), name='submission-status'),
    
    
]