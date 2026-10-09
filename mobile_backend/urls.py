# mobile_backend/urls.py - FINAL WORKING - NO CRASH

from django.contrib import admin
from django.urls import path, include
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView

# Core URLs - always working
urlpatterns = [
    path('admin/', admin.site.urls),

    # ===== API v1 - NEW Versioning =====
    path('api/v1/auth/', include('authentication.urls')),
    path('api/v1/users/', include('authentication.urls')),
    path('api/v1/rides/', include('rides.urls')),

    # ===== OLD API - Backward Compatibility (tests kosam) =====
    path('api/auth/', include('authentication.urls')),
    path('api/users/', include('authentication.urls')),
    path('api/rides/', include('rides.urls')),

    # ===== Docs =====
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('api/docs/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    path('api/docs/v1/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui-v1'),
]

# Optional apps - unte ne add avutayi, lekapothe crash avadu
try:
    urlpatterns += [
        path('api/v1/drivers/', include('rides.urls')),
        path('api/v1/notifications/', include('notifications.urls')),
        path('api/notifications/', include('notifications.urls')),
        path('api/drivers/', include('rides.urls')),
    ]
except Exception:
    # notifications app lekapothe skip
    pass

try:
    urlpatterns += [
        path('api/v1/core/', include('core.urls')),
        path('api/core/', include('core.urls')),
    ]
except Exception:
    pass