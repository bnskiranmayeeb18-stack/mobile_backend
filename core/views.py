from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from django.db import connection

@api_view(['GET'])
@permission_classes([AllowAny])
def health(request):
    return Response({"status":"ok","service":"mobile_backend","version":"1.0"})

@api_view(['GET'])
@permission_classes([AllowAny])
def health_db(request):
    try:
        with connection.cursor() as cur:
            cur.execute("SELECT 1")
        return Response({"status":"ok","database":"connected"})
    except Exception as e:
        return Response({"status":"fail","error": str(e)}, status=503)

@api_view(['GET'])
@permission_classes([AllowAny])
def health_redis(request):
    try:
        from django.core.cache import cache
        cache.set('health','ok',10)
        return Response({"status":"ok","redis":"connected"})
    except Exception as e:
        return Response({"status":"fail"}, status=503)

# For backward compatibility
health_check = health
health_database = health_db
health_celery = health_redis