from django.urls import path
from core.views import health, health_db, health_redis

urlpatterns = [
    path('health/', health, name='health'),
    path('health/database/', health_db, name='health-db'),
    path('health/redis/', health_redis, name='health-redis'),
]