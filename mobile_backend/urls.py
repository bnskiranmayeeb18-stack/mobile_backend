from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/media/', include('media_upload.urls')),
    # If you have other apps, keep them:
    # path('api/', include('core.urls')),
]

# Debug: print URLs
# Run: python manage.py show_urls  (if django-extensions installed)
