from celery import Celery
import logging
logger = logging.getLogger('celery')

app = Celery('mobile_backend')

@app.task(bind=True, max_retries=3)
def monitored_task(self, *args, **kwargs):
    try:
        logger.info(f"TASK_START | task={self.name} | id={self.request.id}")
        # your logic
        logger.info(f"TASK_SUCCESS | task={self.name}")
    except Exception as e:
        logger.error(f"TASK_FAILED | task={self.name} | retry={self.request.retries} | error={str(e)}")
        raise self.retry(exc=e, countdown=60)