celery_log = logging.getLogger('celery')
celery_log.error(f"TASK_FAILED task=send_notification ride_id={ride_id} error={e}")