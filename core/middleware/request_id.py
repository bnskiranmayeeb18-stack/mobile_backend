import uuid
import logging
import threading

_local = threading.local()

class RequestIdFilter(logging.Filter):
    def filter(self, record):
        record.request_id = getattr(_local, 'request_id', 'no-request-id')
        record.user_id = getattr(_local, 'user_id', 'anonymous')
        record.method = getattr(_local, 'method', '-')
        record.endpoint = getattr(_local, 'endpoint', '-')
        record.status_code = getattr(_local, 'status_code', '-')
        record.execution_time = getattr(_local, 'execution_time', '-')
        return True

def get_request_id():
    return getattr(_local, 'request_id', None)

class RequestIdMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
    def __call__(self, request):
        request_id = request.headers.get('X-Request-ID', str(uuid.uuid4())[:8])
        _local.request_id = request_id
        _local.user_id = str(request.user.id) if hasattr(request, 'user') and request.user.is_authenticated else 'anonymous'
        _local.method = request.method
        _local.endpoint = request.path
        response = self.get_response(request)
        response['X-Request-ID'] = request_id
        return response