from django.urls import path
from . import views

urlpatterns = [
    path('api/drivers/location/', views.update_location, name='update-location'),
    path('api/drivers/availability/', views.update_availability, name='update-availability'),
    path('api/admin/driver-locations/', views.admin_driver_locations, name='admin-driver-locations'),
]