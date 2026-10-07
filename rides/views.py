from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from.models import Ride
from.serializers import RideSerializer

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def list_rides(request):
    # FIX: Only own rides - IDOR prevent
    rides = Ride.objects.filter(rider=request.user)
    serializer = RideSerializer(rides, many=True)
    return Response(serializer.data)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_ride(request, ride_id):
    # FIX: IDOR - filter by rider=request.user
    ride = get_object_or_404(Ride, id=ride_id, rider=request.user)
    serializer = RideSerializer(ride)
    return Response(serializer.data)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_ride(request):
    serializer = RideSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save(rider=request.user)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['PUT', 'DELETE'])
@permission_classes([IsAuthenticated])
def update_delete_ride(request, ride_id):
    # FIX: IDOR - only owner can update/delete
    ride = get_object_or_404(Ride, id=ride_id, rider=request.user)
    if request.method == 'PUT':
        serializer = RideSerializer(ride, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    elif request.method == 'DELETE':
        ride.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)