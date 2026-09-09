from django.urls import path
from core import views

urlpatterns = [
    path('api/drivers/location/', views.location_update, name='driver-location'),
    path('api/drivers/availability/', views.availability, name='driver-availability'),
    path('api/drivers/nearby/', views.nearby, name='driver-nearby'),
]