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
    queryset = DriverProfile.objects.select_related('vehicle', 'vehicle__type').all()
    serializer_class = DriverProfileSerializer
    permission_classes = [IsDriverOwnerOrAdmin]

    # Task 5 - Nested Response
    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response({"driver": serializer.data})