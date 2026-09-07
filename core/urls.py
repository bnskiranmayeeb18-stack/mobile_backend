from django.urls import path
from .views import RideStatsView, RideListInefficientView, RideListOptimizedView

urlpatterns = [
    path('stats/', RideStatsView.as_view(), name='ride-stats'),
    path('rides/inefficient/', RideListInefficientView.as_view(), name='rides-inefficient'),
    path('rides/optimized/', RideListOptimizedView.as_view(), name='rides-optimized'),
]