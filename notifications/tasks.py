from celery import shared_task
from .models import Notification
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync

@shared_task
def send_notification_task(user_id, message):
    Notification.objects.create(user_id=user_id, message=message)
    # Real-time push via WebSocket
    channel_layer = get_channel_layer()
    async_to_sync(channel_layer.group_send)(
        f"user_{user_id}",
        {"type": "send_notification", "message": message}
    )