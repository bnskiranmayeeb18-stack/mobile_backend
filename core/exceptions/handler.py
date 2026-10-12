from rest_framework.views import exception_handler
import logging
logger = logging.getLogger('application')

def custom_exception_handler(exc, context):
    response = exception_handler(exc, context)
    request = context.get('request')
    req_id = getattr(request, 'request_id', 'unknown') if request else 'unknown'

    if response is not None:
        error_code = response.data.get('error_code', 'UNKNOWN_ERROR') if isinstance(response.data, dict) else 'UNKNOWN_ERROR'
        message = response.data.get('detail', str(exc)) if isinstance(response.data, dict) else str(exc)

        custom_data = {
            "success": False,
            "message": message,
            "error_code": error_code.upper().replace(' ', '_'),
            "request_id": req_id
        }
        logger.error(f"API_ERROR | req_id={req_id} | {custom_data}")
        response.data = custom_data
    else:
        # 500 errors
        logger.exception(f"UNHANDLED | req_id={req_id}")
        from rest_framework.response import Response
        from rest_framework import status
        return Response({
            "success": False,
            "message": "Internal server error",
            "error_code": "SERVER_ERROR",
            "request_id": req_id
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    return response