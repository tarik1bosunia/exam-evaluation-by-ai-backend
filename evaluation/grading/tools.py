import fitz  # PyMuPDF
import replicate
from evaluation.models import Question, StudentExamSubmission
from langchain_core.tools import tool
from typing import Annotated
from PIL import Image

@tool
def extract_pages_as_images(submission_id: str) -> list[Image.Image]:  # Returns PIL Images
    """Convert PDF submission to PIL Images"""
    try:
        submission = StudentExamSubmission.objects.get(pk=int(submission_id))
        doc = fitz.open(submission.answer_sheet.path)
        images = []
        for i in range(len(doc)):
            page = doc.load_page(i)
            pix = page.get_pixmap(dpi=300)  # Get pixmap from fitz.Page
            img = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)  # Convert to PIL.Image
            images.append(img)
        return images
    except Exception as e:
        raise ValueError(f"PDF processing failed: {str(e)}")

@tool
def analyze_with_florence(
    image: Image.Image,
    question: dict
) -> dict:
    """Analyze handwritten answers using Florence-2-Large"""
    prompt = f"""
    [GRADING INSTRUCTIONS]
    Question {question['id']} ({question['points']} points):
    {question['text']}
    
    Ideal Answer:
    {question['ideal_answer']}
    
    Analyze this handwritten answer and return JSON with:
    - score (0-{question['points']})
    - key_points_covered (list)
    - missing_elements (list)
    - feedback (str)
    """
    
    try:
        output = replicate.run(
            "lucataco/florence-2-large",
            input={
                "image": image,
                "prompt": prompt,
                "structure": "json",
                "max_new_tokens": 1500
            }
        )
        result = eval(output)
        return {
            "question_id": question['id'],
            "score": min(float(result.get("score", 0)), question['points']),
            "feedback": result.get("feedback", "No feedback generated"),
            "key_points": result.get("key_points_covered", []),
            "missing": result.get("missing_elements", [])
        }
    except Exception as e:
        return {
            "question_id": question['id'],
            "error": str(e),
            "score": 0,
            "feedback": "Evaluation failed"
        }