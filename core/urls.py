from django.urls import path
from .views import cancel_ride, create_ride, accept_ride, start_ride, complete_ride

urlpatterns = [
    path('api/rides/create/', create_ride, name='create-ride'),
    path('api/rides/<int:ride_id>/accept/', accept_ride, name='accept-ride'),
    path('api/rides/<int:ride_id>/start/', start_ride, name='start-ride'),
    path('api/rides/<int:ride_id>/complete/', complete_ride, name='complete-ride'),
    path('api/rides/<int:ride_id>/cancel/', cancel_ride, name='cancel-ride'),
]