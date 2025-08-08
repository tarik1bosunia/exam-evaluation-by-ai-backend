from typing import TypedDict, List
from langgraph.graph import StateGraph, END
from django.apps import apps
from PIL import Image
from .tools import analyze_with_florence, extract_pages_as_images

class GradingState(TypedDict):
    submission_id: str
    current_page: int
    page_images: List
    evaluations: List[dict]

def create_grading_workflow():
    Question = apps.get_model('evaluation', 'Question')
    
    workflow = StateGraph(GradingState)

    def extract_images(state: GradingState) -> dict:
        """Node 1: Extract images from PDF"""
        images = extract_pages_as_images.invoke({"submission_id": state["submission_id"]})
        return {"page_images": images, "current_page": 0}
    
    workflow.add_node("extract_images", extract_images)

    def analyze_page(state: GradingState) -> dict:
        """Node 2: Analyze page with Florence-2 (now accepts PIL Image directly)"""
        page_img = state["page_images"][state["current_page"]]  # Already a PIL Image
            
        try:
            # Get question by page number (1-based index)
            question = Question.objects.get(
                exam__submissions=state["submission_id"],
                question_number=state["current_page"] + 1  # Pages are 0-indexed
            )
            
            evaluation = analyze_with_florence.invoke({
                "image": page_img,  # Directly pass PIL Image
                "question": {
                    "id": question.id,
                    "text": question.text,
                    "ideal_answer": question.ideal_answer,
                    "points": question.points
                }
            })
            return {
                "evaluations": state["evaluations"] + [evaluation],
                "current_page": state["current_page"] + 1
            }
        except Question.DoesNotExist:
            return {
                "error": f"No question found for page {state['current_page'] + 1}",
                "current_page": state["current_page"] + 1,
                "evaluations": state["evaluations"]
            }
    
    workflow.add_node("analyze_page", analyze_page)

    def should_continue(state: GradingState) -> str:
        if state["current_page"] < len(state["page_images"]):
            return "analyze_page"
        return "finalize"

    workflow.add_conditional_edges(
        "analyze_page",
        should_continue,
        {"analyze_page": "analyze_page", "finalize": "finalize"}
    )

    def finalize(state: GradingState) -> dict:
        total = sum(e.get("score", 0) for e in state["evaluations"] if isinstance(e, dict))
        return {
            "final_score": total,
            "status": "COMPLETED",
            "evaluations": state["evaluations"]
        }
    
    workflow.add_node("finalize", finalize)
    workflow.add_edge("extract_images", "analyze_page")
    workflow.add_edge("finalize", END)
    workflow.set_entry_point("extract_images")
    
    return workflow.compile()

grading_workflow = create_grading_workflow()