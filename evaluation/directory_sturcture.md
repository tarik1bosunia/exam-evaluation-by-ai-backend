exam_evaluation/
├── config/
│   ├── __init__.py
│   ├── settings.py
│   ├── urls.py
│   └── asgi.py
│   └── wsgi.py
├── evaluation/
│   ├── __init__.py
│   ├── admin.py
│   ├── apps.py
│   ├── models/
│   │   ├── __init__.py
│   │   ├── exam.py
│   │   ├── question.py
│   │   ├── submission.py
│   │   └── answer.py
│   ├── serializers/
│   │   ├── __init__.py
│   │   ├── exam.py
│   │   ├── question.py
│   │   ├── submission.py
│   │   └── answer.py
│   ├── services/
│   │   ├── __init__.py
│   │   ├── file_processing.py
│   │   ├── florence_service.py
│   │   └── ocr_service.py
│   ├── tasks.py
│   ├── urls.py
│   ├── views/
│   │   ├── __init__.py
│   │   ├── exam.py
│   │   ├── question.py
│   │   └── submission.py
│   ├── workflows/
│   │   ├── __init__.py
│   │   └── grading_workflow.py
│   └── utils/
│       ├── __init__.py
│       └── file_utils.py
├── manage.py
├── requirements.txt
└── .env