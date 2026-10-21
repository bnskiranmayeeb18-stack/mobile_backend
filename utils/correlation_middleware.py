import uuid
import logging
import json

logger = logging.getLogger('correlation')

class CorrelationIdMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        corr = request.META.get('HTTP_X_CORRELATION_ID')
        if not corr:
            corr = str(uuid.uuid4())
        request.correlation_id = corr
        request.META['CORRELATION_ID'] = corr
        
        response = self.get_response(request)
        response['X-Correlation-ID'] = corr
        
        log_data = {
            'timestamp': __import__('datetime').datetime.utcnow().isoformat() + 'Z',
            'level': 'info',
            'correlation_id': corr,
            'method': request.method,
            'path': request.get_full_path(),
            'status_code': response.status_code,
            'trace': 'server_boundary'
        }
        logger.info(json.dumps(log_data))
        return response
