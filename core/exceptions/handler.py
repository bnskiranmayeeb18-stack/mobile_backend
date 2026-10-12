import logging
import uuid
from rest_framework.views import exception_handler

logger = logging.getLogger('api')


def custom_exception_handler(exc, context):
    response = exception_handler(exc, context)

    if response is not None:
        request = context.get('request')
        req_id = getattr(request, 'request_id', str(uuid.uuid4())[:8]) if request else str(uuid.uuid4())[:8]

        custom_data = {
            'success': False,
            'message': response.data.get('detail', str(exc)) if isinstance(response.data, dict) else str(response.data),
            'error_code': 'UNKNOWN_ERROR',
            'request_id': req_id
        }

        # Pass request_id via extra to avoid KeyError
        logger.error(f"API_ERROR | req_id={req_id} | {custom_data}", extra={'request_id': req_id})

        response.data = custom_data

    return response