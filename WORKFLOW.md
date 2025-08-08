# High-Level Workflow

- Extract images from the PDF (since Florence is a vision-language model).

- Use Florence-2-Large via Replicate API to analyze each image.

- Use LangChain with LangGraph to orchestrate the pipeline.
