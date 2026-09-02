from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from.services.fare_service import FareService
from.services.ride_service import RideService

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def request_ride(request):
    try:
        data = request.data
        ride = RideService.create_ride(
            customer_name=request.user.username,
            pickup_location=data.get('pickup_location'),
            drop_location=data.get('drop_location'),
            distance_km=float(data.get('distance_km', 0)),
            duration_min=float(data.get('duration_min', 0))
        )
        return Response({"id": ride.id, "fare": ride.fare, "status": ride.status})
    except ValueError as e:
        return Response({"error": str(e)}, status=400)

@api_view(['POST'])
def ride_fare_api(request):
    distance = float(request.data.get('distance_km', 8))
    duration = float(request.data.get('duration_min', 10))
    total_fare = FareService.get_fare_estimate(distance, duration)
    return Response({"total": total_fare})

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def cancel_ride_api(request, ride_id):
    try:
        ride = RideService.cancel_ride(ride_id, request.user)
        return Response({"message": "Cancelled", "status": ride.status})
    except Exception as e:
        return Response({"error": str(e)}, status=400)