from django.urls import path
from.views import health_check, health_database, health_redis, health_celery

urlpatterns = [
    path('health/', health_check, name='health'),
    path('health/database/', health_database, name='health-db'),
    path('health/redis/', health_redis, name='health-redis'),
    path('health/celery/', health_celery, name='health-celery'),
]