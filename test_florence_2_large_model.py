import replicate
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configure your Replicate API token
REPLICATE_API_TOKEN = os.getenv("REPLICATE_API_TOKEN")
if not REPLICATE_API_TOKEN:
    raise ValueError("Please set REPLICATE_API_TOKEN in your .env file")

# Sample question and answer to evaluate
SAMPLE_QUESTION = "What is the derivative of x²?"
IDEAL_ANSWER = "The derivative of x² is 2x."
STUDENT_ANSWER = "I think it's 2x but I'm not sure"

def test_florence_model(question, ideal_answer, student_answer, max_points=5):
    """
    Test the Florence-2 model with a sample question and answer
    """
    prompt = f"""
    Evaluate the student's answer based on the question and ideal answer.
    Provide:
    1. Score (0-{max_points})
    2. Feedback
    3. Confidence (0-1)
    
    Question: {question}
    Ideal Answer: {ideal_answer}
    Student Answer: {student_answer}
    
    Return your evaluation in JSON format with these keys: score, feedback, confidence.
    """
    
    print("\nSending to Florence-2 model...")
    print(f"Question: {question}")
    print(f"Student Answer: {student_answer}")
    
    input = {
    "image": "https://replicate.delivery/pbxt/L9zDhV2KiVnudUyRiNjt9P18LZ98Hrqq5GGdx9szmBCAyEhP/car.jpg",
    "task_input": "Object Detection"
}
    
    try:
        output = replicate.run(
            "lucataco/florence-2-large:da53547e17d45b9cfb48174b2f18af8b83ca020fa76db62136bf9c6616762595",
            input={
                "image": "https://replicate.delivery/pbxt/L9zDhV2KiVnudUyRiNjt9P18LZ98Hrqq5GGdx9szmBCAyEhP/car.jpg",
                "task_input": "Object Detection"
            }
        )
        # Process the output
        full_response = "".join(output)
        print("\nRaw model response:")
        print(full_response)
        
        # Try to extract JSON from the response
        try:
            start_idx = full_response.find('{')
            end_idx = full_response.rfind('}') + 1
            json_str = full_response[start_idx:end_idx]
            
            import json
            result = json.loads(json_str)
            
            print("\nFormatted evaluation:")
            print(f"Score: {result.get('score', 0)}/{max_points}")
            print(f"Confidence: {float(result.get('confidence', 0)):.2f}")
            print(f"Feedback: {result.get('feedback', '')}")
            
        except json.JSONDecodeError:
            print("\nCould not parse JSON response. Full output:")
            print(full_response)
            
    except Exception as e:
        print(f"\nError running Florence-2 model: {e}")

if __name__ == "__main__":
    print("Testing Florence-2 Model Evaluation")
    print("---------------------------------")
    test_florence_model(SAMPLE_QUESTION, IDEAL_ANSWER, STUDENT_ANSWER)