from django.urls import path
from. import views

urlpatterns = [
    # Ride APIs
    path('', views.list_rides, name='ride-list'),
    path('create/', views.create_ride, name='ride-create'),

    # Driver & Vehicle
    path('driver/register/', views.register_driver, name='driver-register'),
    path('vehicle/add/', views.add_vehicle, name='vehicle-add'),

    # Fare & Location
    path('fare/calculate/', views.calculate_fare, name='fare-calc'),
    path('location/update/', views.update_location, name='location-update'),

    # Notifications (Task 7 tests kosam)
    path('notifications/send/', views.send_notification_api, name='notification-send'),
]