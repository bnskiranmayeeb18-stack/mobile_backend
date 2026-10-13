from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.http import JsonResponse

def health_check(request):
    return JsonResponse({"status": "ok"})

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/core/health/', health_check, name='health'),
    path('api/v1/auth/', include('authentication.urls')),
    path('api/v1/rides/', include('rides.urls')),
    path('api/v1/profile/', include('user_profiles.urls')),
    path('api/v1/payments/', include('payments.urls')),
    path('api/rides/', include('rides.urls')),
    path('api/auth/', include('authentication.urls')),
    path('api/', include('user_profiles.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)