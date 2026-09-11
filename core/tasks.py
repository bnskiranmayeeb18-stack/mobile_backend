from celery import shared_task
import time

@shared_task
def test_celery_task():
    time.sleep(2)
    print("Celery Task Executed Successfully!")
    return "Task Done - Redis & Celery Working"