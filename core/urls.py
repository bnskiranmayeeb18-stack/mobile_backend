from django.urls import path
from core import views

urlpatterns = [
    path('api/drivers/availability/', views.DriverAvailabilityView.as_view(), name='driver-availability'),
    path('api/drivers/nearby/', views.NearbyDriverView.as_view(), name='nearby-drivers'),
    path('location/update/', views.DriverLocationUpdateView.as_view()),
    path('availability/', views.DriverAvailabilityView.as_view()),
    path('nearby/', views.NearbyDriverView.as_view()),
]