from langgraph.graph import StateGraph, END
from typing import Dict, Any
from .grading_core import WorkflowState, GradingSystem
from .api_clients import OCRClient, GeminiClient

class GradingWorkflow:
    """Orchestrates the grading pipeline"""
    
    def __init__(self, ocr_client: OCRClient, gemini_client: GeminiClient):
        self.ocr_client = ocr_client
        self.gemini_client = gemini_client
        self.workflow = self._build_workflow()

    def _build_workflow(self):
        """Build the LangGraph workflow"""
        workflow = StateGraph(WorkflowState)
        
        workflow.add_node("ocr_processing", self._process_image_node)
        workflow.add_node("answer_evaluation", self._evaluate_answer_node)
        
        workflow.add_edge("ocr_processing", "answer_evaluation")
        workflow.add_edge("answer_evaluation", END)
        workflow.set_entry_point("ocr_processing")
        
        return workflow.compile()

    def _process_image_node(self, state: WorkflowState) -> Dict[str, Any]:
        """Node for OCR processing"""
        return {"ocr_output": self.ocr_client.process_image(state["image_path"])}

    def _evaluate_answer_node(self, state: WorkflowState) -> Dict[str, Any]:
        """Node for answer evaluation"""
        prompt = GradingSystem.prepare_evaluation_prompt(state)
        response = self.gemini_client.evaluate_answer(prompt)
        return {"evaluation_result": GradingSystem.parse_evaluation_response(response)}

    def run(self, initial_state: WorkflowState) -> Dict[str, Any]:
        """Execute the full workflow"""
        GradingSystem.validate_inputs(initial_state)
        return self.workflow.invoke(initial_state)