from celery import shared_task
from django.core.cache import cache
import logging
logger = logging.getLogger(__name__)
@shared_task
def notify_saved_service_availability_change(service_id, new_availability):
    from .models import SavedService, Service
    try:
        service = Service.objects.get(id=service_id)
        service_name = service.name
    except Service.DoesNotExist:
        service_name = str(service_id)
    saved_list = SavedService.objects.select_related("customer").filter(service_id=service_id)
    count = 0
    for saved in saved_list:
        try:
            try:
                from notifications.models import Notification
                Notification.objects.create(user=saved.customer, message="Service {} is now {}".format(service_name, "available" if new_availability else "unavailable"), type="SAVED_SERVICE_UPDATE")
            except Exception:
                logger.info("Notify user %s: %s", saved.customer_id, service_name)
            count += 1
        except Exception as e:
            logger.error("Failed %s", e)
    return f"Notified {count}"
@shared_task
def debounced_notify(service_id, new_availability):
    cache_key = f"notify_debounce_{service_id}"
    if cache.get(cache_key):
        return "Debounced"
    cache.set(cache_key, True, 300)
    return notify_saved_service_availability_change.delay(service_id, new_availability)
