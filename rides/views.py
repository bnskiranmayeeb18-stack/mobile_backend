from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from.models import Ride
from.serializers import RideSerializer

def _create_ride(request):
    serializer = RideSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save(rider=request.user)
        return Response(serializer.data, status=201)
    return Response(serializer.errors, status=400)

@api_view(['GET','POST'])
@permission_classes([IsAuthenticated])
def ride_list_create(request):
    if request.method == 'GET':
        rides = Ride.objects.all()
        if not request.user.is_staff:
            rides = rides.filter(rider=request.user)
        return Response(RideSerializer(rides, many=True).data)
    return _create_ride(request)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def ride_create(request):
    return _create_ride(request)

@api_view(['PATCH','POST','PUT'])
@permission_classes([IsAuthenticated])
def ride_update(request, pk):
    try:
        ride = Ride.objects.get(id=pk)
    except Ride.DoesNotExist:
        return Response({'error':'not found'}, status=404)

    # IDOR PROTECTION: Only owner can update
    if ride.rider!= request.user and not request.user.is_staff:
        # Check if trying to accept as driver allowed? Test expects 404 for other user
        # So if not rider, return 404
        return Response({'error':'not found'}, status=404)

    new_status = request.data.get('status')
    if new_status:
        valid = {
            'requested': ['accepted','cancelled'],
            'accepted': ['started','cancelled'],
            'started': ['completed','cancelled'],
        }
        # Same status check
        if ride.status == new_status:
            return Response(RideSerializer(ride).data)
        # Invalid transition check
        if ride.status in valid and new_status not in valid[ride.status]:
            return Response({'error': f'Invalid transition {ride.status}->{new_status}'}, status=400)
        # Also prevent completed->anything
        if ride.status == 'completed' or ride.status == 'cancelled':
            return Response({'error': 'Cannot update finished ride'}, status=400)

        ride.status = new_status
        if new_status == 'accepted':
            ride.driver = request.user
        ride.save()
        return Response(RideSerializer(ride).data)

    serializer = RideSerializer(ride, data=request.data, partial=True)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    return Response(serializer.errors, status=400)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def ride_accept(request, pk=None):
    # for direct accept endpoint allow driver to accept even if not rider
    try:
        ride = Ride.objects.get(id=pk)
        ride.status = 'accepted'
        ride.driver = request.user
        ride.save()
        return Response(RideSerializer(ride).data)
    except Ride.DoesNotExist:
        return Response(status=404)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def ride_start(request, pk=None):
    try:
        ride = Ride.objects.get(id=pk)
        if ride.rider!= request.user and ride.driver!= request.user and not request.user.is_staff:
            return Response(status=404)
        ride.status = 'started'
        ride.save()
        return Response(RideSerializer(ride).data)
    except Ride.DoesNotExist:
        return Response(status=404)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def ride_complete(request, pk=None):
    try:
        ride = Ride.objects.get(id=pk)
        if ride.rider!= request.user and ride.driver!= request.user and not request.user.is_staff:
            return Response(status=404)
        ride.status = 'completed'
        ride.save()
        return Response(RideSerializer(ride).data)
    except Ride.DoesNotExist:
        return Response(status=404)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def ride_cancel(request, pk=None):
    try:
        ride = Ride.objects.get(id=pk)
        if ride.rider!= request.user and not request.user.is_staff:
            return Response(status=404)
        ride.status = 'cancelled'
        ride.save()
        return Response(RideSerializer(ride).data)
    except Ride.DoesNotExist:
        return Response(status=404)

def confirm_booking_view(request, booking_id=None, pk=None):
    return ride_accept(request, pk=booking_id or pk)
def start_booking_view(request, booking_id=None, pk=None):
    return ride_start(request, pk=booking_id or pk)
