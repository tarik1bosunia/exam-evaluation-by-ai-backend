exam_evaluator/
├── config/               # Django project folder
│   ├── __init__.py
│   ├── settings/
│   │   ├── base.py       # Shared settings
│   │   ├── local.py      # Dev settings
│   │   └── production.py
│   ├── urls.py
│   └── asgi.py/wsgi.py
│
├── evaluation/           # Main app (create first)
│   ├── __init__.py
│   ├── models/
│   │   ├── __init__.py
│   │   ├── core.py       # Phase 1 models here
│   │   └── extended.py   # Phase 2 models
│   ├── tasks.py          # Celery tasks
│   ├── utils/
│   │   ├── ocr.py        # OCR processors
│   │   └── evaluation.py # LLM grading
│   └── admin.py
│
├── media/                # User uploads
│   ├── answer_scripts/
│   └── script_pages/
│
└── templates/
    └── evaluation/
        ├── upload.html   # First template to create
        └── results.html