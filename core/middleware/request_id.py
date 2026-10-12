import uuid
import logging
from django.utils.deprecation import MiddlewareMixin

logger_api = logging.getLogger('api')
logger = logging.getLogger(__name__)


class RequestIDMiddleware(MiddlewareMixin):
    def __call__(self, request):
        # Generate request_id
        request_id = str(uuid.uuid4())[:8]
        request.request_id = request_id

        # Attach to thread local for logging
        import threading
        threading.current_thread().request_id = request_id

        response = self.get_response(request)

        # Add to response header
        response['X-Request-ID'] = request_id

        # Log slow APIs
        try:
            import time
            start = getattr(request, '_start_time', None)
            if start:
                duration = (time.time() - start) * 1000
                if duration > 1000:  # >1 sec
                    user_id = getattr(request.user, 'id', 'anonymous') if hasattr(request, 'user') else 'anonymous'
                    log_data = {
                        'timestamp': __import__('datetime').datetime.utcnow().isoformat() + 'Z',
                        'request_id': request_id,
                        'user_id': str(user_id),
                        # logger_api.warning(f"SLOW API | {log_data}")  # comment this
                        'method': request.method,
                        'status': response.status_code,
                        'duration_ms': round(duration, 2)
                    }
                    logger_api.warning(f"SLOW API | {log_data}", extra={'request_id': request_id})
        except:
            pass

        return response

    def process_view(self, request, view_func, view_args, view_kwargs):
        import time
        request._start_time = time.time()
        return None