import uuid
import time
import logging
import contextvars

request_id_ctx = contextvars.ContextVar('request_id', default=None)
logger_api = logging.getLogger('api')
logger_app = logging.getLogger('application')

class RequestIDMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        req_id = request.headers.get('X-Request-ID', str(uuid.uuid4())[:8])
        request.request_id = req_id
        request_id_ctx.set(req_id)
        request.start_time = time.time()

        response = self.get_response(request)

        duration = (time.time() - request.start_time) * 1000
        user_id = getattr(request.user, 'id', None) if hasattr(request, 'user') and request.user.is_authenticated else 'anonymous'

        log_data = {
            "timestamp": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
            "request_id": req_id,
            "user_id": str(user_id),
            "endpoint": request.path,
            "method": request.method,
            "status": response.status_code,
            "duration_ms": round(duration, 2),
        }

        if duration > 500:
            logger_api.warning(f"SLOW API | {log_data}")
        else:
            logger_api.info(f"{log_data}")

        response['X-Request-ID'] = req_id
        return response