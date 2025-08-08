from celery import shared_task
from evaluation.workflows.grading_workflow import grading_workflow
from evaluation.models import StudentExamSubmission

@shared_task(bind=True, max_retries=3)
def grade_submission_task(self, submission_id):
    submission = StudentExamSubmission.objects.get(pk=submission_id)
    
    try:
        workflow = grading_workflow()
        workflow.invoke({"submission_id": str(submission.id)})
    except Exception as e:
        submission.status = "ERROR"
        submission.save()
        raise self.retry(exc=e, countdown=60)