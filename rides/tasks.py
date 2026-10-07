import logging

from celery import shared_task
from django.core.cache import cache

from notifications.models import Notification

logger = logging.getLogger(__name__)


@shared_task(bind=True, max_retries=3, default_retry_delay=5)
def send_ride_notification(self, ride_id, event_type, message):
    lock_key = f"notif_lock:ride:{ride_id}:{event_type}"

    if cache.get(lock_key):
        print(f"DUPLICATE PREVENTED: Ride {ride_id} - {event_type}")
        return "Duplicate prevented"

    try:
        if Notification.objects.filter(ride_id=ride_id, event_type=event_type).exists():
            cache.set(lock_key, True, timeout=60)
            print(f"Duplicate in DB - Prevented for Ride {ride_id}")
            return "Duplicate prevented - exists in DB"

        Notification.objects.create(
            ride_id=ride_id, event_type=event_type, message=message
        )
        cache.set(lock_key, True, timeout=60)

        print(f"SUCCESS: Notification sent for Ride {ride_id} - {event_type}")
        return f"Notification sent for ride {ride_id}"

    except Exception as exc:
        print(f"Attempt {self.request.retries + 1} Failed, retrying...")
        raise self.retry(exc=exc)
