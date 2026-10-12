from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from.models import Ride, DriverProfile
from.serializers import RideSerializer

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_ride(request):
    data = request.data
    if not data.get('pickup') or not data.get('drop'):
        return Response({"pickup":"required","drop":"required"}, status=400)
    ride = Ride.objects.create(
        rider=request.user,
        pickup=data.get('pickup'),
        drop=data.get('drop'),
        status='requested'
    )
    return Response(RideSerializer(ride).data, status=201)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def list_rides(request):
    rides = Ride.objects.filter(rider=request.user)
    return Response(RideSerializer(rides, many=True).data)

@api_view(['PUT', 'PATCH'])
@permission_classes([IsAuthenticated])
def update_ride(request, ride_id):
    # IDOR: only owner can update - return 404 if not owner
    ride = Ride.objects.filter(id=ride_id, rider=request.user).first()
    if not ride:
        return Response({"detail":"Not found"}, status=404)
    new_status = request.data.get('status')
    valid = {
        'requested': ['accepted','cancelled'],
        'accepted': ['started','cancelled'],
        'started': ['completed','cancelled'],
        'completed': [],
        'cancelled': []
    }
    if new_status and new_status not in valid.get(ride.status, []):
        return Response({'error':'invalid transition'}, status=400)
    if new_status:
        ride.status = new_status
        ride.save()
    return Response(RideSerializer(ride).data, status=200)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def my_rides(request):
    rides = Ride.objects.filter(rider=request.user)
    return Response(RideSerializer(rides, many=True).data)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def driver_toggle(request):
    p,_ = DriverProfile.objects.get_or_create(user=request.user)
    p.is_online = not p.is_online
    p.save()
    return Response({'is_online': p.is_online})
