from django.urls import path
from .views import optimized_rides, ride_stats, ride_list, ride_history
urlpatterns = [
    path('rides/', ride_list, name='ride-list'),
    path('rides/optimized/', optimized_rides, name='optimized-rides'),
    path('rides/stats/', ride_stats, name='ride-stats'),
    path('rides/history/', ride_history, name='ride-history'),
]