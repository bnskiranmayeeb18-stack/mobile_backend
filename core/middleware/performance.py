import time
import logging
logger_db = logging.getLogger('database')

class PerformanceMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
    def __call__(self, request):
        start = time.time()
        response = self.get_response(request)
        duration = (time.time() - start)*1000
        if duration > 1000:
            logger_db.warning(f"DB_SLOW | {request.path} | {duration:.2f}ms")
        return response