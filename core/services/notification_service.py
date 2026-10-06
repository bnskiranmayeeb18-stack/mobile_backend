"""
NotificationService - Notification logic moved from views - Task 3 fix
"""
from django.core.cache import cache
import uuid

class NotificationService:
    @staticmethod
    def send_notification(user, ride, message):
        from notifications.models import Notification
        # Idempotency - duplicate prevention
        idempotency_key = f"{user.id}_{ride.id}_{message}"
        if Notification.objects.filter(idempotency_key=idempotency_key).exists():
            return None # Already sent - no duplicate

        notification = Notification.objects.create(
            user=user,
            ride=ride,
            message=message,
            idempotency_key=idempotency_key
        )
        # Invalidate cache
        cache.delete(f"notifications_{user.id}")
        return notification

    @staticmethod
    def send_ride_created(user, ride):
        return NotificationService.send_notification(user, ride, f"Ride {ride.id} created")

    @staticmethod
    def send_status_update(user, ride, status):
        return NotificationService.send_notification(user, ride, f"Ride {ride.id} status: {status}")