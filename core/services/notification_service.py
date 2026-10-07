import logging

logger = logging.getLogger(__name__)


class NotificationService:
    @staticmethod
    def send_notification(user, message, ride=None):
        logger.info(f"Notification to {user.id}: {message}")
        from core.models import Notification

        notification = Notification.objects.create(
            user=user,
            message=message,
            ride=ride,
        )
        return notification

    @staticmethod
    def get_user_notifications(user):
        from core.models import Notification

        return Notification.objects.filter(user=user).order_by("-created_at")

    @staticmethod
    def mark_as_read(notification_id, user):
        from core.models import Notification

        try:
            notification = Notification.objects.get(
                id=notification_id, user=user
            )
            notification.is_read = True
            notification.save()
            return notification
        except Notification.DoesNotExist:
            return None
