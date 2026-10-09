import time
from celery import shared_task
import logging
logger = logging.getLogger(__name__)

@shared_task(bind=True, autoretry_for=(Exception,), retry_kwargs={'max_retries': 3, 'countdown': 5}, queue='notifications')
def send_notification(self, user_id, message):
    logger.info(f"[NOTIFICATIONS] Sending to user {user_id}: {message}")
    time.sleep(1)
    return f"Notification sent to {user_id}"

@shared_task(bind=True, autoretry_for=(Exception,), retry_kwargs={'max_retries': 2, 'countdown': 10}, queue='reports')
def generate_ride_report(self, date_str=None):
    logger.info(f"[REPORTS] Generating for {date_str}")
    time.sleep(2)
    return f"Report generated for {date_str}"

@shared_task(bind=True, autoretry_for=(Exception,), retry_kwargs={'max_retries': 3, 'countdown': 5}, queue='maintenance')
def clean_expired_data(self):
    logger.info("[MAINTENANCE] Cleaning expired data")
    return "Cleaned expired data"

@shared_task(bind=True, autoretry_for=(Exception,), retry_kwargs={'max_retries': 3, 'countdown': 5}, queue='maintenance')
def process_background_records(self, record_id):
    logger.info(f"[MAINTENANCE] Processing {record_id}")
    return f"Processed {record_id}"

@shared_task
def test_celery_task():
    time.sleep(2)
    print("Celery Task Executed Successfully!")
    return "Task Done - Redis and Celery Working"