from celery import Celery
from app.config import settings

celery_app = Celery(
    "taskflow",
    broker=settings.BROKER_URL,
    backend=settings.RESULT_BACKEND,
)

celery_app.conf.update(
    task_serializer="json",
    accept_content=["json"],
    result_serializer="json",
)

import app.background_tasks

celery_app.conf.beat_schedule = {
    "distribute-tasks-every-10-seconds": {
        "task": "app.background_tasks.distribute_tasks",
        "schedule": 10.0,  # Кожні 10 секунд
    },
}

celery_app.conf.timezone = "UTC"