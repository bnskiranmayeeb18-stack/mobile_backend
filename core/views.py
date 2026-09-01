from rest_framework import viewsets
from .models import DriverProfile, Vehicle, VehicleType, Ride, RideLocation
from .serializers import (
    DriverProfileSerializer,
    VehicleSerializer,
    VehicleTypeSerializer,
    RideSerializer,
    RideLocationSerializer
)

class DriverProfileViewSet(viewsets.ModelViewSet):
    queryset = DriverProfile.objects.all()
    serializer_class = DriverProfileSerializer

class VehicleViewSet(viewsets.ModelViewSet):
    queryset = Vehicle.objects.all()
    serializer_class = VehicleSerializer

class VehicleTypeViewSet(viewsets.ModelViewSet):
    queryset = VehicleType.objects.all()
    serializer_class = VehicleTypeSerializer

class RideViewSet(viewsets.ModelViewSet):
    queryset = Ride.objects.all()
    serializer_class = RideSerializer

class RideLocationViewSet(viewsets.ModelViewSet):
    queryset = RideLocation.objects.all()
    serializer_class = RideLocationSerializer