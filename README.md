# AnswerIQ
Answers evaluated with intelligence

Taking handwritten exam answer scripts → extracting text via OCR → evaluating answers using an LLM (like Gemini) → based on provided questions, answers, and mark distribution.

---

# workflow summery
### 📄 Exam Evaluation Pipeline

1. **Receive handwritten PDF**
2. **Convert to image (one per page)**
3. **(Optional) OCR to extract text**
4. **Feed question, marking scheme, and image to Florence-2-Large**
5. **Model returns score and reasoning**
6. **Display or store result**
pip install pdf2image
pip install pytesseract

# Procedure
1. [initial procedures(virtualenv)](./guides/initial/INITIAL.md)

# TODO
- make ayncronous all , try to use celery, work like background task
- upload pdf, make image