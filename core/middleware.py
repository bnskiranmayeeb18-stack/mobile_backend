import uuid
import logging
import json
from django.utils.deprecation import MiddlewareMixin

logger = logging.getLogger('correlation')

class CorrelationIdMiddleware(MiddlewareMixin):
    """
    Day 4 - Observability: Structured correlation IDs
    - Reads X-Correlation-ID from request or generates new uuid4
    - Adds to response header
    - Adds to request.META for views
    - Structured JSON logging
    """
    CORRELATION_HEADER = 'HTTP_X_CORRELATION_ID'
    RESPONSE_HEADER = 'X-Correlation-ID'

    def process_request(self, request):
        correlation_id = request.META.get(self.CORRELATION_HEADER)
        if not correlation_id:
            correlation_id = str(uuid.uuid4())
        
        request.correlation_id = correlation_id
        request.META['CORRELATION_ID'] = correlation_id
        return None

    def process_response(self, request, response):
        correlation_id = getattr(request, 'correlation_id', None) or request.META.get('CORRELATION_ID', str(uuid.uuid4()))
        response[self.RESPONSE_HEADER] = correlation_id
        
        # Structured log - traceable across client/server
        log_data = {
            "timestamp": __import__('datetime').datetime.utcnow().isoformat() + "Z",
            "level": "info",
            "correlation_id": correlation_id,
            "method": request.method,
            "path": request.get_full_path(),
            "status_code": response.status_code,
            "trace": "server_boundary"
        }
        logger.info(json.dumps(log_data))
        
        # Optional: also print for dev
        print(json.dumps(log_data))
        return response
