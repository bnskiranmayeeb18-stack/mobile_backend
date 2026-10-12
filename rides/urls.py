from django.urls import path
from .views import RideCreateView, RideAcceptView, RideStatusView, DriverLocationView, DriverOnlineView

urlpatterns = [
    path('', RideCreateView.as_view(), name='ride-create'),  # POST /api/v1/rides/
    path('<int:ride_id>/accept/', RideAcceptView.as_view(), name='ride-accept'),
    path('<int:ride_id>/status/', RideStatusView.as_view(), name='ride-status'),
    path('driver/location/', DriverLocationView.as_view(), name='driver-location'),
    path('driver/online/', DriverOnlineView.as_view(), name='driver-online'),
]