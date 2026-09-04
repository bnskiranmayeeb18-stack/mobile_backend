from django.urls import path
from.views import register_customer, login_view, create_ride, ride_status_update, ride_detail

urlpatterns = [
    path('api/register/', register_customer, name='register'),
    path('api/login/', login_view, name='login'),
    path('api/rides/create/', create_ride, name='create-ride'),
    path('api/rides/<int:ride_id>/status/', ride_status_update, name='ride-status-update'),
    path('api/rides/<int:ride_id>/', ride_detail, name='ride-detail'),
]