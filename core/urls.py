from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path("admin/", admin.site.urls),
    path(
        "api/v1/auth/",
        include("apps.authentication.urls"),
    ),
    path(
        "api/v1/users/",
        include("apps.users.urls"),
    ),
    path(
        "api/v1/drivers/",
        include("apps.drivers.urls"),
    ),
    path(
        "api/v1/rides/",
        include("apps.rides.urls"),
    ),
    path(
        "api/v1/notifications/",
        include("apps.notifications.urls"),
    ),
    path("api/", include("core.services.urls")),
]
