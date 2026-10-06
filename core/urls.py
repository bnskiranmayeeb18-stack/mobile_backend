from django.urls import path
from .views import get_ride, get_notifications

urlpatterns = [
    # IMPORTANT: notifications mundhu undali
    path('notifications/', get_notifications, name='get_notifications'),
    path('<str:ride_id>/', get_ride, name='get_ride'),
]