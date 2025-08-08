from django.urls import path
from .views import FileUploadView, ExamCreateView, ExamListView, ExamDetailView

urlpatterns = [
    path('upload/', FileUploadView.as_view(), name='pdf-upload'),
    path('exams/create/', ExamCreateView.as_view(), name='exam-create'),
    path('exams/', ExamListView.as_view(), name='exam-list'),
    path('exams/<int:pk>/', ExamDetailView.as_view(), name='exam-detail')
]
