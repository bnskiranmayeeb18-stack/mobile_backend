
import hashlib, json
from functools import wraps
from django.utils import timezone
from rest_framework.response import Response
from .models import IdempotencyKey

def get_django_request(request):
    # Unwrap DRF Request to Django HttpRequest if needed
    return getattr(request, '_request', request) or getattr(request, 'request', request)

def get_key(request):
    dj_req = get_django_request(request)
    # Try DRF headers first, then META
    try:
        k = request.headers.get('Idempotency-Key')
        if k:
            return k
    except:
        pass
    return dj_req.META.get('HTTP_IDEMPOTENCY_KEY') or dj_req.headers.get('Idempotency-Key')

def hash_body(request):
    try:
        dj_req = get_django_request(request)
        body = getattr(dj_req, 'body', b'') or b''
        return hashlib.sha256(body).hexdigest()
    except:
        return ''

def idempotent(view_func):
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        key = get_key(request)
        if not key:
            return view_func(request, *args, **kwargs)
        
        user = getattr(request, 'user', None)
        if not user or not user.is_authenticated:
            return view_func(request, *args, **kwargs)

        body_hash = hash_body(request)
        dj_req = get_django_request(request)
        method = getattr(dj_req, 'method', getattr(request, 'method', 'POST'))
        path = getattr(dj_req, 'get_full_path', lambda: getattr(request, 'path', '/'))()
        try:
            path = dj_req.get_full_path()
        except:
            path = getattr(request, 'path', '/')

        try:
            existing = IdempotencyKey.objects.get(user=user, key=key)
            if existing.body_hash == body_hash and existing.response_body:
                try:
                    data = json.loads(existing.response_body)
                    return Response(data, status=existing.response_code or 200)
                except:
                    pass
            if existing.response_body:
                try:
                    data = json.loads(existing.response_body)
                    return Response(data, status=existing.response_code or 200)
                except:
                    pass
        except IdempotencyKey.DoesNotExist:
            existing = None

        if not existing:
            try:
                existing = IdempotencyKey.objects.create(
                    user=user,
                    key=key,
                    method=method,
                    path=path,
                    body_hash=body_hash,
                )
            except Exception:
                try:
                    existing = IdempotencyKey.objects.get(user=user, key=key)
                    if existing.response_body:
                        data = json.loads(existing.response_body)
                        return Response(data, status=existing.response_code or 200)
                except:
                    pass

        response = view_func(request, *args, **kwargs)

        try:
            resp_code = getattr(response, 'status_code', 200)
            resp_data = getattr(response, 'data', None)
            if resp_data is None:
                try:
                    resp_data = json.loads(response.content)
                except:
                    resp_data = {}
            IdempotencyKey.objects.filter(id=existing.id).update(
                response_code=resp_code,
                response_body=json.dumps(resp_data, default=str),
            )
        except Exception as e:
            print(f"idempotency save error: {e}")

        return response
    return wrapper
