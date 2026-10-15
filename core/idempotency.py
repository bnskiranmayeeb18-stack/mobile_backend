# core/idempotency.py
import hashlib, json
from functools import wraps
from django.utils import timezone
from rest_framework.response import Response
from.models import IdempotencyKey

def get_request_hash(data):
    try:
        body = json.dumps(data, sort_keys=True)
    except:
        body = str(data)
    return hashlib.sha256(body.encode()).hexdigest()

def idempotent(view_func):
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        key = request.headers.get('Idempotency-Key') or request.META.get('HTTP_IDEMPOTENCY_KEY')
        if not key:
            return view_func(request, *args, **kwargs)

        req_hash = get_request_hash(request.data if hasattr(request, 'data') else {})

        try:
            existing = IdempotencyKey.objects.get(key=key, user=request.user)
            if existing.is_expired():
                existing.delete()
            else:
                if existing.request_hash!= req_hash:
                    return Response({'error':'Idempotency key reuse with different payload'}, status=409)
                # replay
                import json as js
                return Response(js.loads(existing.response_body), status=existing.response_status)
        except IdempotencyKey.DoesNotExist:
            pass

        response = view_func(request, *args, **kwargs)

        # store only for 2xx/4xx
        if response.status_code < 500:
            try:
                IdempotencyKey.objects.create(
                    key=key, user=request.user,
                    method=request.method, path=request.path,
                    request_hash=req_hash,
                    response_status=response.status_code,
                    response_body=json.dumps(response.data) if hasattr(response, 'data') else str(response.data)
                )
            except:
                pass
        return response
    return wrapper
