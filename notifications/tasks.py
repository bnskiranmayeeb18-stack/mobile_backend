from celery import shared_task
from .models import Notification
import logging

logger = logging.getLogger(__name__)

@shared_task
def driver_accepts_ride_task(user_id, ride_id=None):
    try:
        message = f"Driver accepted your ride #{ride_id}" if ride_id else "Driver accepted your ride"
        Notification.objects.create(user_id=user_id, message=message)
        logger.info(f"Notification created for user {user_id}: {message}")
        return f"Sent: {message}"
    except Exception as e:
        logger.error(f"Error in driver_accepts_ride_task: {e}")
        return str(e)

@shared_task
def driver_arrives_task(user_id, ride_id=None):
    try:
        message = f"Driver has arrived for ride #{ride_id}" if ride_id else "Driver has arrived"
        Notification.objects.create(user_id=user_id, message=message)
        logger.info(f"Notification created for user {user_id}: {message}")
        return f"Sent: {message}"
    except Exception as e:
        logger.error(f"Error in driver_arrives_task: {e}")
        return str(e)

@shared_task
def ride_starts_task(user_id, ride_id=None):
    try:
        message = f"Your ride #{ride_id} has started" if ride_id else "Your ride has started"
        Notification.objects.create(user_id=user_id, message=message)
        return f"Sent: {message}"
    except Exception as e:
        return str(e)

@shared_task
def ride_completes_task(user_id, ride_id=None):
    try:
        message = f"Your ride #{ride_id} is completed" if ride_id else "Your ride is completed"
        Notification.objects.create(user_id=user_id, message=message)
        return f"Sent: {message}"
    except Exception as e:
        return str(e)

@shared_task
def ride_cancelled_task(user_id, ride_id=None):
    try:
        message = f"Your ride #{ride_id} has been cancelled" if ride_id else "Your ride has been cancelled"
        Notification.objects.create(user_id=user_id, message=message)
        return f"Sent: {message}"
    except Exception as e:
        return str(e)