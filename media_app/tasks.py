import logging
from celery import shared_task
from django.db import transaction
from .models import MediaAsset

logger = logging.getLogger(__name__)

@shared_task(bind=True, max_retries=3, autoretry_for=(Exception,), retry_backoff=True, retry_backoff_max=600)
def process_media(self, media_id: str, correlation_id: str = ""):
    log_extra = {"correlation_id": correlation_id, "media_id": media_id}
    
    try:
        with transaction.atomic():
            media = MediaAsset.objects.select_for_update().get(id=media_id)
            
            # Idempotency: avoid duplicate processing results
            if media.processing_status == MediaAsset.Status.READY:
                logger.info("processing-skip-already-ready", extra=log_extra)
                return {"status": "already_ready", "media_id": str(media.id)}
            
            if media.processing_status == MediaAsset.Status.PROCESSING:
                logger.info("processing-skip-already-processing", extra=log_extra)
                return {"status": "already_processing", "media_id": str(media.id)}

            media.processing_status = MediaAsset.Status.PROCESSING
            media.save(update_fields=["processing_status", "updated_at"])
        
        logger.info(f"event: processing-started media_id={media_id} correlation_id={correlation_id}", extra=log_extra)
        
        # --- THUMBNAIL / TRANSCODE LOGIC HERE ---
        
        with transaction.atomic():
            media = MediaAsset.objects.select_for_update().get(id=media_id)
            media.processing_status = MediaAsset.Status.READY
            media.save(update_fields=["processing_status", "updated_at"])
        
        logger.info(f"event: processing-completed media_id={media_id} correlation_id={correlation_id}", extra=log_extra)
        return {"status": "completed", "media_id": str(media.id)}

    except MediaAsset.DoesNotExist:
        logger.error(f"event: processing-failed-not-found media_id={media_id}", extra=log_extra)
        return {"status": "failed", "reason": "not_found"}
        
    except Exception as e:
        logger.error(f"event: processing-failed media_id={media_id} error={str(e)} correlation_id={correlation_id}", extra=log_extra)
        with transaction.atomic():
            try:
                media = MediaAsset.objects.select_for_update().get(id=media_id)
                media.processing_status = MediaAsset.Status.FAILED
                media.error_message = str(e)[:500]
                media.save(update_fields=["processing_status", "error_message", "updated_at"])
            except:
                pass
        raise self.retry(exc=e)