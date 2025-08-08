import replicate
import base64
import os
from langchain_google_genai import ChatGoogleGenerativeAI
from typing import Dict, Any

class OCRClient:
    """Client for Florence-2 OCR service"""
    
    def __init__(self, api_token: str):
        self.client = replicate.Client(api_token=api_token)
    
    def process_image(self, image_path: str) -> Dict[str, Any]:
        """Process image with Florence-2 OCR"""
        if not os.path.exists(image_path):
            raise FileNotFoundError(f"Image file not found at: {image_path}")

        with open(image_path, "rb") as f:
            image_data = f.read()
            base64_image = base64.b64encode(image_data).decode("utf-8")

        return self.client.run(
            "lucataco/florence-2-large:da53547e17d45b9cfb48174b2f18af8b83ca020fa76db62136bf9c6616762595",
            input={
                "image": f"data:image/png;base64,{base64_image}",
                "task_input": "OCR"
            }
        )

class GeminiClient:
    """Client for Gemini evaluation service"""
    
    def __init__(self, api_key: str):
        self.llm = ChatGoogleGenerativeAI(
            model="gemini-2.0-flash",
            temperature=0.3,
            max_output_tokens=1000,
            api_key=api_key,
        )
    
    def evaluate_answer(self, prompt: str) -> str:
        """Evaluate answer using Gemini"""
        response = self.llm.invoke(prompt)
        return response.content