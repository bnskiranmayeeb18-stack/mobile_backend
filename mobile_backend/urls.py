from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('core.urls')),  # <-- IDI IMPORTANT - HEALTH CHECK
    path('api/v1/rides/', include('rides.urls')),
    path('api/v1/notifications/', include('notifications.urls')),
]