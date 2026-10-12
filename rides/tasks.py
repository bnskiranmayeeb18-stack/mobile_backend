from celery import shared_task
import logging, time
logger = logging.getLogger('celery')

@shared_task(bind=True, max_retries=3)
def notify_drivers_task(self, ride_id, drivers):
    try:
        logger.info(f"Notifying {len(drivers)} drivers for ride {ride_id}")
        time.sleep(1)
        # Simulate notification
        return f"Notified {len(drivers)} drivers"
    except Exception as e:
        logger.error(f"notify failed {e}, retrying")
        raise self.retry(exc=e, countdown=5)

@shared_task(bind=True, max_retries=3)
def notify_passenger_task(self, ride_id, event):
    logger.info(f"Passenger notification ride={ride_id} event={event}")
    return True

@shared_task
def ride_summary_task(ride_id):
    logger.info(f"Ride summary generated for {ride_id}")
    return True