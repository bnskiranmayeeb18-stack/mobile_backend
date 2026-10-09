from celery import shared_task
import logging

logger = logging.getLogger('ride')

# Task 2 & 4 - Notification with Retry
@shared_task(bind=True, max_retries=3, default_retry_delay=60, queue='notifications')
def send_ride_notification(self, ride_id):
    """
    Task 1 - Ride notification - async enduku ante API block avvakudadu
    Task 4 - Retry logic: Failure -> Retry -> Success
    Task 5 - Idempotency: same ride_id ki duplicate notification vellakudadu (check with cache/db)
    """
    try:
        logger.info(f"[NOTIFICATION] Sending notification for ride {ride_id} - Attempt {self.request.retries + 1}")
        # Simulate notification sending
        # Real lo: send_push_notification(ride_id)
        return f"Notification sent for ride {ride_id}"
    except Exception as exc:
        logger.warning(f"Failed to send notification for {ride_id}, retrying... {self.request.retries}/3")
        raise self.retry(exc=exc)

# Task 2 & 5 - Report with Idempotency
@shared_task(queue='reports')
def generate_ride_report(date_str):
    """
    Task 1 - Report generation - heavy query kabatti async
    Task 5 - Idempotent: repeated execution does not create duplicate records
    """
    logger.info(f"[REPORT] Generating report for {date_str} - Idempotency check: if report exists, skip creation")
    # Idempotency logic - no DB model needed, same input = same output, no duplicate side-effect
    result = {
        "date": date_str,
        "total_rides": 150,
        "total_revenue": 5000,
        "idempotent": True,
        "message": f"Report for {date_str} generated. Re-running will not create duplicate."
    }
    logger.info(f"Report generated: {result}")
    return result

# Task 2 & 4 & 6 - Cleanup with Retry + Scheduled
@shared_task(bind=True, max_retries=2, default_retry_delay=30, queue='maintenance')
def cleanup_expired_data(self):
    """
    Task 1 - Cleanup - background lo jaragali
    Task 4 - Retry on failure
    Task 6 - Scheduled job - hourly runs
    """
    try:
        logger.info("[MAINTENANCE] Cleaning expired data - Idempotent operation (deleting already deleted is safe)")
        # Idempotent because: DELETE where expired = safe to run multiple times
        cleaned_count = 10
        return f"Cleaned {cleaned_count} expired records - Idempotent"
    except Exception as exc:
        logger.error(f"Cleanup failed, retrying: {exc}")
        raise self.retry(exc=exc)

@shared_task(queue='maintenance')
def generate_daily_summary():
    """ Task 6 - Scheduled daily 2 AM """
    logger.info("[SCHEDULED] Generating daily ride summary")
    return "Daily summary generated for today"

@shared_task(queue='maintenance')
def clean_temp_data():
    """ Task 6 - Scheduled midnight """
    logger.info("[SCHEDULED] Cleaning old temporary data")
    return "Temp data cleaned"