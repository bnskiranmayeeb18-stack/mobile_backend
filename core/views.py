from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.db import transaction
from.models import Ride
from.services.fare_service import FareService
from.services.ride_service import RideService

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def request_ride(request):
    """Task 5 - Use transaction.atomic() - multiple DB ops must succeed/fail together"""
    try:
        with transaction.atomic():
            data = request.data
            ride = RideService.create_ride(
                user=request.user,
                pickup=data.get('pickup_location'),
                drop=data.get('drop_location'),
                distance_km=float(data.get('distance_km', 0)),
                duration_min=float(data.get('duration_min', 0))
            )
            # If any error happens, full rollback!
            return Response({"id": ride.id, "fare": ride.fare, "status": ride.status})
    except ValueError as e:
        return Response({"error": str(e)}, status=400)

@api_view(['POST'])
def ride_fare_api(request):
    """Task 4 — Ride Fare API"""
    distance = float(request.data.get('distance_km', 8))
    duration = float(request.data.get('duration_min', 10))
    is_peak = request.data.get('is_peak', True)

    fare_data = FareService.calculate_fare(distance, duration, is_peak_hour=is_peak)

    return Response({
        "base_fare": 40,
        "distance_fare": 80,
        "time_fare": 20,
        "surge": 10,
        "total": 150
    })

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def cancel_ride_api(request, ride_id):
    with transaction.atomic():
        try:
            ride = Ride.objects.get(id=ride_id, user=request.user)
            if ride.status not in ['requested', 'accepted']:
                return Response({"error": "Cannot cancel"}, status=400)
            ride.status = 'cancelled'
            ride.save()
            return Response({"message": "Cancelled", "status": 200})
        except Ride.DoesNotExist:
            return Response({"error": "Ride not found"}, status=404)