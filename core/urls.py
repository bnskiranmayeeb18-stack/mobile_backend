from django.urls import path
from .views import cancel_ride

urlpatterns = [
    path('api/rides/<int:ride_id>/cancel/', cancel_ride, name='cancel-ride'),
]