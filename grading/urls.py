from django.urls import path
from .views import GradingJobView

urlpatterns = [
    path("run-hardcoded-grading/", GradingJobView.as_view(), name="run_hardcoded_grading"),
]
