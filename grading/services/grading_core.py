from typing import TypedDict, Dict, Any
import json

class WorkflowState(TypedDict):
    """Defines the structure of the workflow state"""
    image_path: str
    ocr_output: dict
    question: str
    ideal_answer: str
    max_points: int
    criteria: str
    evaluation_result: dict

class GradingSystem:
    """Core logic for OCR and answer evaluation"""
    
    @staticmethod
    def validate_inputs(state: WorkflowState) -> None:
        """Validate required inputs"""
        if not state.get("image_path"):
            raise ValueError("Image path is required")
        if not state.get("question"):
            raise ValueError("Question is required")
        if not state.get("ideal_answer"):
            raise ValueError("Ideal answer is required")
        if not state.get("max_points"):
            raise ValueError("Max points is required")
        if not state.get("criteria"):
            raise ValueError("Grading criteria is required")

    @staticmethod
    def prepare_evaluation_prompt(state: WorkflowState) -> str:
        """Generate the evaluation prompt"""
        return f"""
        **Grading Task**:
        You are an expert teacher grading a student's handwritten answer. 
        You will receive the raw OCR output from a scanned answer sheet.

        **Question**: {state["question"]}
        **Ideal Answer**: {state["ideal_answer"]}
        **Max Points**: {state["max_points"]}
        **Grading Criteria**: {state["criteria"]}

        **Raw OCR Output**:
        {json.dumps(state["ocr_output"], indent=2)}

        **Instructions**:
        1. Analyze the OCR output to find the student's answer
        2. Compare it to the ideal answer
        3. Apply the grading criteria strictly
        4. Return JSON with:
           - extracted_answer (the text you identified)
           - score (0-{state["max_points"]})
           - feedback (specific improvements needed)
           - breakdown (points awarded per criteria)
           - confidence (0-100% how sure you are in your extraction)

        **Required JSON Format**:
        {{
            "extracted_answer": string,
            "score": number,
            "feedback": string,
            "breakdown": [
                {{
                    "criteria": string,
                    "points_awarded": number,
                    "comments": string
                }}
            ],
            "confidence": number
        }}
        """

    @staticmethod
    def parse_evaluation_response(response: str) -> Dict[str, Any]:
        """Parse the evaluation response into structured data"""
        try:
            json_str = response[response.find('{'):response.rfind('}')+1]
            return json.loads(json_str)
        except json.JSONDecodeError:
            return {
                "error": "Invalid JSON response",
                "raw_response": response,
                "score": 0,
                "feedback": "Evaluation failed - invalid response format"
            }