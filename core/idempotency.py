import json
from functools import wraps
from django.core.cache import cache
from rest_framework.response import Response

def get_django_request(request):
    # DRF Request ayite _request lo HttpRequest untadi, lekapote ade HttpRequest
    return getattr(request, '_request', request)

def get_key(request):
    # DRF request.headers nundi, lekapote META nundi
    key = None
    if hasattr(request, 'headers'):
        key = request.headers.get('Idempotency-Key')
    if not key:
        dj_req = get_django_request(request)
        key = dj_req.META.get('HTTP_IDEMPOTENCY_KEY') or dj_req.META.get('HTTP_IDEMPOTENCY-KEY')
    return key

def idempotent(view_func):
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        key = get_key(request)
        if not key:
            # Key lekapote normal ga continue
            return view_func(request, *args, **kwargs)

        user_id = getattr(request.user, 'id', 'anon') if hasattr(request, 'user') else 'anon'
        cache_key = f"idem:{user_id}:{key}"

        cached = cache.get(cache_key)
        if cached:
            # Duplicate request - same response return, DB hit avadu
            return Response(cached['data'], status=cached['status'])

        # First time
        response = view_func(request, *args, **kwargs)

        # Only cache success responses
        if response.status_code < 400:
            cache.set(cache_key, {
                'data': response.data,
                'status': response.status_code
            }, timeout=60*60*24) # 24 hours

        return response
    return wrapper