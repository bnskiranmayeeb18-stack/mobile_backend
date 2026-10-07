import logging

from celery_app import shared_task

from .models import Notification

logger = logging.getLogger(__name__)

# ============ TASK 6 - 5 Background Tasks ============


@shared_task
def driver_accepts_ride_task(user_id, ride_id=None):
    try:
        message = (
            f"Driver accepted your ride #{ride_id}"
            if ride_id
            else "Driver accepted your ride"
        )
        Notification.objects.create(user_id=user_id, message=message)
        logger.info(f"Notification: {message}")
        return f"Sent: {message}"
    except Exception as e:
        logger.error(f"Error: {e}")
        return str(e)


@shared_task
def driver_arrives_task(user_id, ride_id=None):
    try:
        message = (
            f"Driver has arrived for ride #{ride_id}"
            if ride_id
            else "Driver has arrived"
        )
        Notification.objects.create(user_id=user_id, message=message)
        return f"Sent: {message}"
    except Exception as e:
        return str(e)


@shared_task
def ride_starts_task(user_id, ride_id=None):
    try:
        message = (
            f"Your ride #{ride_id} has started" if ride_id else "Your ride has started"
        )
        Notification.objects.create(user_id=user_id, message=message)
        return f"Sent: {message}"
    except Exception as e:
        return str(e)


@shared_task
def ride_completes_task(user_id, ride_id=None):
    try:
        message = (
            f"Your ride #{ride_id} is completed"
            if ride_id
            else "Your ride is completed"
        )
        Notification.objects.create(user_id=user_id, message=message)
        return f"Sent: {message}"
    except Exception as e:
        return str(e)


@shared_task
def ride_cancelled_task(user_id, ride_id=None):
    try:
        message = (
            f"Your ride #{ride_id} has been cancelled"
            if ride_id
            else "Your ride has been cancelled"
        )
        Notification.objects.create(user_id=user_id, message=message)
        return f"Sent: {message}"
    except Exception as e:
        return str(e)


# ============ TASK 7 - Retry Failed Tasks ============


@shared_task(bind=True, max_retries=3, default_retry_delay=5)
def retry_failed_notification_task(self, user_id, ride_id=None):
    attempt_number = self.request.retries + 1
    print(
        f"Attempt {attempt_number} -> {'Failed' if attempt_number < 3 else 'Success'}"
    )

    try:
        if attempt_number < 3:
            raise Exception(f"Simulated failure on attempt {attempt_number}")

        message = (
            f"Notification delivered after {attempt_number} attempts for ride #{ride_id}"
            if ride_id
            else f"Notification delivered after {attempt_number} attempts"
        )
        Notification.objects.create(user_id=user_id, message=message)
        print(f"Attempt {attempt_number} -> Success")
        return f"Success on attempt {attempt_number}: {message}"

    except Exception as exc:
        if attempt_number < 3:
            print(f"Retrying... attempt {attempt_number} failed, retrying in 5 sec")
            raise self.retry(exc=exc, countdown=5)
        else:
            raise exc
