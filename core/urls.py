# mobile_backend/urls.py - Task 7 FINAL - API v1 organized
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),

    # Task 7 - API v1 - Organized by responsibility
    path('api/v1/auth/', include('apps.authentication.urls')),          # /api/v1/auth/login/, /api/v1/auth/register/
    path('api/v1/users/', include('apps.users.urls')),                   # /api/v1/users/, /api/v1/users/<id>/
    path('api/v1/drivers/', include('apps.drivers.urls')),               # /api/v1/drivers/nearby/, /api/v1/drivers/<id>/
    path('api/v1/rides/', include('apps.rides.urls')),                   # /api/v1/rides/, /api/v1/rides/create/
    path('api/v1/notifications/', include('apps.notifications.urls')),   # /api/v1/notifications/

    # Old - Keep backward compatibility - Redirect to v1
    path('api/', include('core.services.urls')), # nee old urls - temporary
]

# For DRF browsable API title
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi