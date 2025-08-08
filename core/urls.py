from django.urls import path
from .views import FileUploadView, ExamCreateView

urlpatterns = [
    path('upload/', FileUploadView.as_view(), name='pdf-upload'),
    path('exams/create/', ExamCreateView.as_view(), name='exam-create'),
    
]
