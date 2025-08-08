from grading.models import GradingJob
from grading.services import OCRClient, GeminiClient, GradingWorkflow, WorkflowState
from django.conf import settings


def execute_grading_job(
    image_path: str,
    question: str,
    ideal_answer: str,
    max_points: int,
    grading_criteria: str
) -> GradingJob:
    """Creates and processes a grading job and returns the saved model instance."""

    # Create the DB record
    job = GradingJob.objects.create(
        image=image_path,  # if not a file field, consider File mock or skip
        question=question,
        ideal_answer=ideal_answer,
        criteria=grading_criteria,
        max_points=max_points
    )

    # Initialize clients and workflow
    ocr_client = OCRClient(settings.REPLICATE_API_TOKEN)
    gemini_client = GeminiClient(settings.GEMINI_API_KEY)
    workflow = GradingWorkflow(ocr_client, gemini_client)

    # Define initial state
    initial_state: WorkflowState = {
        "image_path": image_path,
        "question": question,
        "ideal_answer": ideal_answer,
        "max_points": max_points,
        "criteria": grading_criteria,
        "ocr_output": None,
        "evaluation_result": None
    }

    # Run pipeline
    result = workflow.run(initial_state)

    # Save results
    job.ocr_output = result.get("ocr_output")
    job.evaluation_result = result.get("evaluation_result")
    job.save()

    return job
