import uuid
import time
import logging

logger = logging.getLogger('api')

class RequestIDMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        request_id = request.headers.get('X-Request-ID', str(uuid.uuid4())[:8])
        request.request_id = request_id
        request.start_time = time.time()
        response = self.get_response(request)
        duration = (time.time() - request.start_time) * 1000
        user_id = getattr(request.user, 'id', 'anonymous') if hasattr(request, 'user') and getattr(request.user, 'is_authenticated', False) else 'anonymous'
        logger.info(f"[{request_id}] [{user_id}] {request.method} {request.path} {response.status_code} {duration:.2f}ms")
        response['X-Request-ID'] = request_id
        response['X-Execution-Time'] = f"{duration:.2f}ms"
        if duration > 500:
            logger.warning(f"SLOW API [{request_id}] {request.method} {request.path} took {duration:.2f}ms")
        return response