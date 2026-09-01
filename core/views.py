from rest_framework import viewsets
from rest_framework.response import Response
from.models import VehicleType, Vehicle, DriverProfile
from.serializers import VehicleTypeSerializer, VehicleSerializer, DriverProfileSerializer
from.permissions import IsAdminOrReadOnly, IsDriverOwnerOrAdmin

class VehicleTypeViewSet(viewsets.ModelViewSet):
    queryset = VehicleType.objects.all()
    serializer_class = VehicleTypeSerializer
    permission_classes = [IsAdminOrReadOnly]

class VehicleViewSet(viewsets.ModelViewSet):
    queryset = Vehicle.objects.all()
    serializer_class = VehicleSerializer
    permission_classes = [IsAdminOrReadOnly]

class DriverProfileViewSet(viewsets.ModelViewSet):
    serializer_class = DriverProfileSerializer

    def get_queryset(self):
        queryset = DriverProfile.objects.all()
        is_active = self.request.query_params.get('is_active')
        if is_active is not None:
            if is_active.lower() == 'true':
                queryset = queryset.filter(is_active=True)
            elif is_active.lower() == 'false':
                queryset = queryset.filter(is_active=False)
        return queryset