from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import Ride  # or DriverRide? Nee model name pettu


@api_view(['POST'])
def cancel_ride(request, ride_id):
    try:
        ride = Ride.objects.get(id=ride_id)
    except Ride.DoesNotExist:
        return Response({"error": "Ride not found"}, status=404)

    if ride.status in ['COMPLETED', 'STARTED']:
        return Response({"error": f"Cannot cancel a {ride.status} ride"}, status=400)

    if ride.status == 'CANCELLED':
        return Response({"error": "Ride is already cancelled"}, status=400)

    ride.status = 'CANCELLED'
    ride.save()
    return Response({"message": "Ride cancelled successfully", "ride_id": ride.id, "status": ride.status}, status=200)