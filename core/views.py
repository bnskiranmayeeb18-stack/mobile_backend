from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from django.db import connection
from django.core.cache import cache
from django.conf import settings
import time
import logging
import redis

logger = logging.getLogger('application')

@api_view(['GET'])
@permission_classes([AllowAny])
def health_check(request):
    logger.info(f"[{getattr(request, 'request_id', 'no-id')}] Health check OK")
    return Response({
        "status": "ok",
        "timestamp": time.time(),
        "request_id": getattr(request, 'request_id', 'no-id'),
        "service": "mobile_backend",
        "version": "1.0"
    })

@api_view(['GET'])
@permission_classes([AllowAny])
def health_database(request):
    try:
        with connection.cursor() as cursor:
            cursor.execute("SELECT 1")
        return Response({"status": "ok", "database": "connected", "request_id": getattr(request, 'request_id', 'no-id')})
    except Exception as e:
        logger.error(f"DB Health Failed: {e}")
        return Response({"status": "error", "database": "disconnected", "error": "Database unavailable"}, status=503)

@api_view(['GET'])
@permission_classes([AllowAny])
def health_redis(request):
    try:
        cache.set('health_check', 'ok', 10)
        val = cache.get('health_check')
        if val == 'ok':
            return Response({"status": "ok", "redis": "connected", "request_id": getattr(request, 'request_id', 'no-id')})
        raise Exception("Redis mismatch")
    except Exception as e:
        logger.error(f"Redis Health Failed: {e}")
        return Response({"status": "error", "redis": "disconnected", "error": "Redis unavailable"}, status=503)

@api_view(['GET'])
@permission_classes([AllowAny])
def health_celery(request):
    try:
        from mobile_backend.celery import app
        inspect = app.control.inspect()
        stats = inspect.stats()
        if not stats:
            return Response({"status": "warning", "celery": "no workers", "request_id": getattr(request, 'request_id', 'no-id')}, status=200)
        return Response({"status": "ok", "celery": "running", "workers": list(stats.keys()), "request_id": getattr(request, 'request_id', 'no-id')})
    except Exception as e:
        logger.error(f"Celery Health Failed: {e}")
        return Response({"status": "error", "celery": "unavailable", "error": str(e)}, status=503)