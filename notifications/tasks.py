from celery import shared_task
import logging
logger = logging.getLogger('api')

@shared_task(bind=True, queue='notifications', max_retries=3)
def send_notification(self, user_id, message):
    try:
        logger.info(f"[NOTIF] To user {user_id}: {message}")
        return f"Sent to {user_id}"
    except Exception as exc:
        raise self.retry(exc=exc, countdown=60)
