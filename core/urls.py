from django.urls import path
from.views import request_ride, ride_fare_api, cancel_ride_api

urlpatterns = [
    path('api/rides/request/', request_ride, name='request-ride'),
    path('api/fare-estimate/', ride_fare_api, name='ride-fare-api'),
    path('api/rides/<int:ride_id>/cancel/', cancel_ride_api, name='cancel-ride'),
]