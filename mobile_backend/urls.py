# mobile_backend/mobile_backend/urls.py - Task 7 FIXED
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),

    # Task 7 - Apps have clear responsibilities + API v1 versioning - WORKING
    # NOTE: rides existing ga undi - danike main focus
    path('api/v1/rides/', include('rides.urls')),

    # Migatha apps - ippatiki comment lo petta - ModuleNotFoundError rakunda
    # Neev create chesina folders path correct ayyaka uncomment cheyyi
    # path('api/v1/auth/', include('core.authentication.urls')),
    # path('api/v1/users/', include('core.users.urls')),
    # path('api/v1/drivers/', include('core.drivers.urls')),
    # path('api/v1/notifications/', include('core.notifications.urls')),
]