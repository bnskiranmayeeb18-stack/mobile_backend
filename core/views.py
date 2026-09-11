from rest_framework.decorators import api_view
from rest_framework.response import Response
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
from.models import Ride
import json
from django.contrib.auth import authenticate
from rest_framework.authtoken.models import Token

# Task 7 - Token API (for WebSocket auth)
@api_view(['POST'])
def get_token(request):
    username = request.data.get('username')
    password = request.data.get('password')
    user = authenticate(username=username, password=password)
    if user:
        token, _ = Token.objects.get_or_create(user=user)
        return Response({'token': token.key, 'username': user.username})
    return Response({'error': 'Invalid credentials'}, status=400)

# Task 4 - Status update API
@api_view(['POST'])
def update_ride_status(request, ride_id):
    try:
        ride = Ride.objects.get(id=ride_id)
        new_status = request.data.get('status')

        if not new_status:
            return Response({'error': 'status field required'}, status=400)

        # Valid status check


        ride.status = new_status
        ride.save()


        # WebSocket broadcast
        channel_layer = get_channel_layer()
        async_to_sync(channel_layer.group_send)(
            f"ride_{ride_id}",
            {
                "type": "ride_status_update",
                "status": new_status,
                "ride_id": str(ride_id)
            }
        )

        return Response({'status': new_status, 'ride_id': str(ride_id)})

    except Ride.DoesNotExist:
        return Response({'error': 'Ride not found'}, status=404)
    except Exception as e:
        return Response({'error': str(e)}, status=500)

@api_view(['POST'])
def update_driver_location(request, ride_id):
    try:
        ride = Ride.objects.get(id=ride_id)
        lat = request.data.get('lat')
        lng = request.data.get('lng')

        channel_layer = get_channel_layer()
        async_to_sync(channel_layer.group_send)(
            f"ride_{ride_id}",
            {
                "type": "driver_location_update",
                "lat": lat,
                "lng": lng,
                "ride_id": str(ride_id)
            }
        )
        return Response({'lat': lat, 'lng': lng})
    except Ride.DoesNotExist:
        return Response({'error': 'Ride not found'}, status=404)

@api_view(['GET'])
def get_ride(request, ride_id):
    try:
        ride = Ride.objects.get(id=ride_id)
        return Response({
            'id': str(ride.id),
            'status': ride.status,
            'driver': ride.driver.username if ride.driver else None
        })
    except Ride.DoesNotExist:
        return Response({'error': 'Ride not found'}, status=404)