from django.urls import path
from. import views

urlpatterns = [
    path('<str:ride_id>/status/', views.update_ride_status),
    path('<str:ride_id>/location/', views.update_driver_location),
    path('<str:ride_id>/', views.get_ride),
]