from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from.models import Ride, DriverProfile
from.serializers import RideSerializer, DriverProfileSerializer, VehicleSerializer
from.models import Vehicle

class VehicleViewSet(viewsets.ModelViewSet):
    queryset = Vehicle.objects.all()
    serializer_class = VehicleSerializer
    permission_classes = [IsAuthenticated]

class DriverProfileViewSet(viewsets.ModelViewSet):
    queryset = DriverProfile.objects.all()
    serializer_class = DriverProfileSerializer
    permission_classes = [IsAuthenticated]

class RideViewSet(viewsets.ModelViewSet):
    queryset = Ride.objects.all()
    serializer_class = RideSerializer
    permission_classes = [IsAuthenticated]

    @action(detail=True, methods=['post'], url_path='accept')
    def accept_ride(self, request, pk=None):
        ride = self.get_object()
        # Ride already accepted aithe 200 ivvu, 403 kadu
        if ride.status == 'accepted' and ride.driver:
            return Response({"id": ride.id, "status": ride.status, "driver": ride.driver.user.username, "message": "Already accepted"})

        driver, _ = DriverProfile.objects.get_or_create(
            user=request.user,
            defaults={'license_number': 'AUTO123', 'phone': '9999999999', 'is_available': True, 'is_active': True}
        )
        ride.driver = driver
        ride.status = 'accepted'
        ride.save()
        return Response({"id": ride.id, "status": "accepted", "driver": request.user.username})

    @action(detail=True, methods=['post'], url_path='complete')
    def complete_ride(self, request, pk=None):
        ride = self.get_object()
        ride.status = 'completed'
        ride.save()
        return Response({"id": ride.id, "status": "completed"})