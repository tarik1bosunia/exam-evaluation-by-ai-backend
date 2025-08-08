import replicate
import os
from django.conf import settings
from typing import Dict, Any

class FlorenceService:
    def __init__(self):
        self.client = replicate.Client(api_token=os.getenv('REPLICATE_API_TOKEN'))
    
    def evaluate_answer(self, question: str, ideal_answer: str, student_answer: str, max_points: int) -> Dict[str, Any]:
        prompt = f"""
        Evaluate the student's answer based on the question and ideal answer.
        Provide a score from 0 to {max_points}, feedback, and confidence (0-1).
        
        Question: {question}
        Ideal Answer: {ideal_answer}
        Student Answer: {student_answer}
        
        Return in JSON format with keys: score, feedback, confidence.
        """
        
        try:
            output = self.client.run(
                "lucataco/florence-2-large:f38f768a8c8a9c1a5c4d9a5e4f7d0e0d7d7c9e5d5a5e4f7d0e0d7d7c9e5d5a5e4f7d0e0d",
                input={
                    "prompt": prompt,
                    "max_new_tokens": 1024,
                    "temperature": 0.7,
                }
            )
            
            # Process the output to extract JSON
            full_output = "".join(output)
            start_idx = full_output.find('{')
            end_idx = full_output.rfind('}') + 1
            json_output = full_output[start_idx:end_idx]
            
            import json
            result = json.loads(json_output)
            
            return {
                'score': min(max_points, float(result.get('score', 0))),
                'feedback': result.get('feedback', ''),
                'confidence': min(1.0, max(0.0, float(result.get('confidence', 0))))
            }
        except Exception as e:
            print(f"Florence-2 evaluation failed: {e}")
            return {
                'score': 0,
                'feedback': 'Evaluation failed',
                'confidence': 0
            }