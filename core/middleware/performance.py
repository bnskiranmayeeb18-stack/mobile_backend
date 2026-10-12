import time
import logging
logger = logging.getLogger('api')
slow_logger = logging.getLogger('application')
from.request_id import _local

class PerformanceMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
    def __call__(self, request):
        start = time.time()
        response = self.get_response(request)
        duration = (time.time() - start) * 1000
        _local.execution_time = f"{duration:.2f}"
        _local.status_code = response.status_code
        logger.info(f"{request.method} {request.path} - {response.status_code} - {duration:.2f}ms")
        if duration > 500:
            slow_logger.warning(f"SLOW API: {request.method} {request.path} took {duration:.2f}ms")
        response['X-Response-Time'] = f"{duration:.2f}ms"
        return response