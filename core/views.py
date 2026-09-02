# CANCEL - Nee code (already correct)
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import Ride


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


# --- TASK 8 KE KAVALSINA MIGATHA APIS ---

@api_view(['POST'])
def create_ride(request):
    try:
        data = request.data
        ride = Ride.objects.create(
            customer_name=data.get('customer_name', 'Kiranmayee Test'),
            pickup_location=data.get('pickup', 'Vizag'),
            drop_location=data.get('drop', 'Rushikonda'),
            ride_type=data.get('ride_type', 'STANDARD'),
            passenger_info={"passenger_id": data.get('passenger_id', 1)},
            status='REQUESTED'
        )
        return Response({"message": "Ride created", "ride_id": ride.id, "status": ride.status}, status=201)
    except Exception as e:
        return Response({"error": str(e)}, status=500)


@api_view(['POST'])
def accept_ride(request, ride_id):
    try:
        ride = Ride.objects.get(id=ride_id)
    except Ride.DoesNotExist:
        return Response({"error": "Ride not found"}, status=404)

    if ride.status != 'REQUESTED':
        return Response({"error": f"Cannot accept ride in {ride.status} status"}, status=400)

    # driver assign cheyadam optional - model lo driver nullable aithe
    if ride.driver is None:
        # first driver ni assign cheddam test kosam
        from .models import DriverProfile
        first_driver = DriverProfile.objects.first()
        if first_driver:
            ride.driver = first_driver

    ride.status = 'ACCEPTED'
    ride.save()
    return Response({"message": "Ride accepted", "ride_id": ride.id, "status": ride.status}, status=200)

@api_view(['POST'])
def start_ride(request, ride_id):
    try:
        ride = Ride.objects.get(id=ride_id)
    except Ride.DoesNotExist:
        return Response({"error": "Ride not found"}, status=404)

    if ride.status != 'ACCEPTED':
        return Response({"error": f"Cannot start ride in {ride.status} status"}, status=400)

    ride.status = 'STARTED'
    ride.save()
    return Response({"message": "Ride started", "ride_id": ride.id, "status": ride.status}, status=200)


@api_view(['POST'])
def complete_ride(request, ride_id):
    try:
        ride = Ride.objects.get(id=ride_id)
    except Ride.DoesNotExist:
        return Response({"error": "Ride not found"}, status=404)

    if ride.status != 'STARTED':
        return Response({"error": f"Cannot complete ride in {ride.status} status"}, status=400)

    ride.status = 'COMPLETED'
    ride.save()
    return Response({"message": "Ride completed", "ride_id": ride.id, "status": ride.status}, status=200)