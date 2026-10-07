"""
helpers.py - Most repeated code in project - cache, idempotency, cache invalidation
"""

import hashlib

from django.core.cache import cache


def get_cache_or_db(cache_key, db_func, ttl=1800):
    # MOST REPEATED CODE - cache.get + DB + cache.set - Used in every service
    data = cache.get(cache_key)
    if data is not None:
        return data, True  # True = cache HIT
    data = db_func()
    cache.set(cache_key, data, timeout=ttl)
    return data, False  # False = cache MISS


def invalidate_cache_patterns(patterns):
    # Repeated cache.delete in many places
    for pattern in patterns:
        if "*" in pattern:
            # Redis pattern delete
            try:
                cache.delete_pattern(pattern)
            except:
                cache.delete(pattern)
        else:
            cache.delete(pattern)


def generate_idempotency_key(*args):
    # Repeated idempotency_key generation - notifications, rides
    raw = "_".join([str(a) for a in args])
    return hashlib.md5(raw.encode()).hexdigest()


def get_client_ip(request):
    xff = request.META.get("HTTP_X_FORWARDED_FOR")
    if xff:
        return xff.split(",")[0]
    return request.META.get("REMOTE_ADDR")


# This will be used for Task 6 also
def build_success_response(message, data=None):
    return {
        "success": True,
        "message": message,
        "data": data if data is not None else {},
    }


def build_error_response(message, errors=None, code=None):
    return {
        "success": False,
        "message": message,
        "errors": errors if errors else {},
        "code": code,
    }
