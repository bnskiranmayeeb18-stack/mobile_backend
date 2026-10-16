import logging
import uuid
from celery import shared_task
from django.db import transaction

logger = logging.getLogger(__name__)

@shared_task(bind=True, max_retries=3)
def process_media(self, media_id, correlation_id=None):
    from .models import MediaFile
    cid = correlation_id or str(uuid.uuid4())
    try:
        logger.info(f"processing-started | correlation_id={cid} | media_id={media_id}", extra={"correlation_id": cid, "media_id": str(media_id)})
        with transaction.atomic():
            media = MediaFile.objects.select_for_update().get(id=media_id)
            if media.status == MediaFile.Status.COMPLETED:
                logger.info(f"already completed, skipping | correlation_id={cid}", extra={"correlation_id": cid})
                return
            media.status = MediaFile.Status.PROCESSING
            media.save()

        # simulate processing
        media.status = MediaFile.Status.COMPLETED
        media.save()
        logger.info(f"processing-completed | correlation_id={cid}", extra={"correlation_id": cid, "media_id": str(media_id)})

    except Exception as e:
        logger.error(f"processing-failed | correlation_id={cid} | error={e}", extra={"correlation_id": cid, "media_id": str(media_id)})
        try:
            media = MediaFile.objects.get(id=media_id)
            media.status = MediaFile.Status.FAILED
            media.error_message = str(e)
            media.save()
        except:
            pass
        raise self.retry(exc=e, countdown=2**self.request.retries)