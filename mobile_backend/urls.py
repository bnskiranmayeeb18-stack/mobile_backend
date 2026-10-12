from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('core.urls')),  # HEALTH CHECK
    path('api/health/', include('core.urls')),
    path('api/v1/auth/', include('authentication.urls')),
    path('api/v1/rides/', include('rides.urls')),
    path('api/v1/notifications/', include('notifications.urls')),
    path('api/v1/rides/', include('rides.urls')),
    path('api/health/', include('core.urls')),
]