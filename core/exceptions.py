from rest_framework.views import exception_handler
import logging

logger = logging.getLogger('application')

def custom_exception_handler(exc, context):
    request = context.get('request')
    request_id = getattr(request, 'request_id', 'no-id') if request else 'no-id'
    response = exception_handler(exc, context)
    if response is not None:
        status = response.status_code
        if status == 404:
            code = "NOT_FOUND"
            msg = "Resource not found"
        elif status == 401:
            code = "UNAUTHORIZED"
            msg = "Authentication required"
        elif status == 403:
            code = "FORBIDDEN"
            msg = "Permission denied"
        elif status == 400:
            code = "BAD_REQUEST"
            msg = response.data.get('detail', 'Invalid request') if isinstance(response.data, dict) else str(response.data)
        elif status == 429:
            code = "RATE_LIMITED"
            msg = "Too many requests"
        else:
            code = f"ERROR_{status}"
            msg = "An error occurred"

        # Special case for Ride not found
        if 'Ride' in str(response.data):
            msg = "Ride not found"
            code = "RIDE_NOT_FOUND"

        custom = {
            "success": False,
            "message": msg,
            "error_code": code,
            "request_id": request_id
        }
        response.data = custom
        logger.error(f"[{request_id}] {status} {code} - {msg} | Path: {request.path if request else 'unknown'}")
    return response