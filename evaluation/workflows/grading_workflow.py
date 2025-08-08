from typing import TypedDict, Annotated, Sequence
import operator
from langgraph.graph import StateGraph, END
from evaluation.services import file_processing, ocr_service, florence_service
from evaluation.models import StudentExamSubmission, Question, Answer
from django.utils import timezone

class WorkflowState(TypedDict):
    submission_id: str
    images: Annotated[Sequence[str], operator.add]
    current_page: int
    ocr_text: str
    evaluation_results: dict

def grading_workflow():
    workflow = StateGraph(WorkflowState)
    
    workflow.add_node("start_grading", start_grading)
    workflow.add_node("convert_pdf", convert_pdf)
    workflow.add_node("check_pages", check_pages)
    workflow.add_node("perform_ocr", perform_ocr)
    workflow.add_node("evaluate", evaluate)
    workflow.add_node("store_results", store_results)
    workflow.add_node("generate_report", generate_report)
    
    workflow.set_entry_point("start_grading")
    workflow.add_edge("start_grading", "convert_pdf")
    workflow.add_edge("convert_pdf", "check_pages")
    
    workflow.add_conditional_edges(
        "check_pages",
        decide_next_page,
        {
            "more_pages": "perform_ocr",
            "no_more_pages": "evaluate"
        }
    )
    
    workflow.add_edge("perform_ocr", "check_pages")
    workflow.add_edge("evaluate", "store_results")
    workflow.add_edge("store_results", "generate_report")
    workflow.add_edge("generate_report", END)
    
    return workflow.compile()

def start_grading(state: WorkflowState):
    submission = StudentExamSubmission.objects.get(pk=state["submission_id"])
    submission.status = "PROCESSING"
    submission.processing_start_time = timezone.now()
    submission.save()
    return {"submission_id": state["submission_id"]}

def convert_pdf(state: WorkflowState):
    submission = StudentExamSubmission.objects.get(pk=state["submission_id"])
    pdf_path = submission.answer_sheet.path
    images = file_processing.convert_pdf_to_images(pdf_path)
    return {"images": images, "current_page": 0}

def check_pages(state: WorkflowState):
    if state["current_page"] < len(state["images"]) - 1:
        return "more_pages"
    return "no_more_pages"

def perform_ocr(state: WorkflowState):
    current_page = state["current_page"] + 1
    ocr_text = ocr_service.extract_text_from_image(state["images"][current_page])
    return {
        "current_page": current_page,
        "ocr_text": ocr_text
    }

def evaluate(state: WorkflowState):
    submission = StudentExamSubmission.objects.get(pk=state["submission_id"])
    exam = submission.exam
    florence = florence_service.FlorenceService()
    
    for question in exam.questions.all():
        evaluation = florence.evaluate_answer(
            question.text,
            question.ideal_answer,
            state["ocr_text"],
            question.points
        )
        
        Answer.objects.create(
            submission=submission,
            question=question,
            extracted_text=state["ocr_text"],
            image_path=state["images"][0],
            score=evaluation["score"],
            feedback=evaluation["feedback"],
            confidence=evaluation["confidence"]
        )
    
    return {"evaluation_results": "completed"}

def store_results(state: WorkflowState):
    submission = StudentExamSubmission.objects.get(pk=state["submission_id"])
    
    total_score = sum(
        answer.score for answer in submission.answers.all()
        if answer.score is not None
    )
    max_score = submission.exam.total_points
    
    submission.score = (total_score / max_score) * 100 if max_score > 0 else 0
    submission.status = "GRADED"
    submission.processing_end_time = timezone.now()
    submission.save()
    
    # Cleanup temporary files
    file_processing.cleanup_temp_files(state["images"])
    
    return state

def generate_report(state: WorkflowState):
    # Placeholder for report generation
    return state

def decide_next_page(state: WorkflowState):
    if state["current_page"] < len(state["images"]) - 1:
        return "more_pages"
    return "no_more_pages"