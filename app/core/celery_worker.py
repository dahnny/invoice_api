from celery import Celery
import time
import app.tasks.email


celery_app = Celery(
    "invoice_api",
    broker="redis://localhost:6379/0",
    backend="redis://localhost:6379/0",
    include=["app.tasks.email"],
)



