from django.urls import path
from.views import update_driver_location, register, login

urlpatterns = [
    path('api/register/', register, name='register'),
    path('api/login/', login, name='login'),
    path('api/drivers/location/', update_driver_location, name='update-driver-location'),
]