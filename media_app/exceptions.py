from rest_framework.views import exception_handler
import logging
logger = logging.getLogger(__name__)

def custom_exception_handler(exc, context):
    response = exception_handler(exc, context)
    if response is not None:
        correlation_id = getattr(context.get('request'), 'correlation_id', '')
        response.data = {
            "error": {
                "code": response.status_code,
                "message": str(exc.detail) if hasattr(exc, 'detail') else str(exc),
                "correlation_id": correlation_id
            }
        }
        logger.warning(f"api_error status={response.status_code} error={response.data} correlation_id={correlation_id}")
    return response