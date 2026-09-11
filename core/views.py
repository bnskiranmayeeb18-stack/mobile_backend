from rest_framework.decorators import api_view
from rest_framework.response import Response
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
from.models import Ride
import json

# Task 4 - Status update API
@api_view(['POST'])
def update_ride_status(request, ride_id):
    try:
        ride = Ride.objects.get(id=ride_id)
        new_status = request.data.get('status')

        if not new_status:
            return Response({'error': 'status field required'}, status=400)

        # Valid status check
        valid_statuses = [s[0] for s in Ride.STATUS_CHOICES]
        if new_status not in valid_statuses:
            return Response({'error': f'Invalid status. Valid: {valid_statuses}'}, status=400)

        ride.status = new_status
        ride.save()

        # WebSocket lo broadcast
        channel_layer = get_channel_layer()
        async_to_sync(channel_layer.group_send)(
            f'ride_{ride_id}',
            {
                'type': 'ride_status',
                'status': new_status
            }
        )

        return Response({
            'ride_id': str(ride.id),
            'status': ride.status,
            'message': 'Status updated'
        })

    except Ride.DoesNotExist:
        return Response({'error': 'Ride not found'}, status=404)
    except Exception as e:
        return Response({'error': str(e)}, status=500)

# Task 5 - Driver Location Update API
@api_view(['POST'])
def update_driver_location(request, ride_id):
    try:
        ride = Ride.objects.get(id=ride_id)

        lat = request.data.get('lat')
        lng = request.data.get('lng')
        heading = request.data.get('heading', 0)

        if lat is None or lng is None:
            return Response({'error': 'lat and lng required'}, status=400)

        ride.driver_lat = float(lat)
        ride.driver_lng = float(lng)
        ride.driver_heading = float(heading) if heading else 0
        ride.save()

        # WebSocket lo Passenger ki pampadam
        channel_layer = get_channel_layer()
        async_to_sync(channel_layer.group_send)(
            f'ride_{ride_id}',
            {
                'type': 'driver_location',
                'lat': ride.driver_lat,
                'lng': ride.driver_lng,
                'heading': ride.driver_heading
            }
        )

        return Response({
            'ride_id': str(ride.id),
            'lat': ride.driver_lat,
            'lng': ride.driver_lng,
            'heading': ride.driver_heading,
            'message': 'location updated and broadcasted'
        })

    except Ride.DoesNotExist:
        return Response({'error': 'Ride not found'}, status=404)
    except Exception as e:
        return Response({'error': str(e)}, status=500)

# Optional - Ride create / get
@api_view(['GET'])
def get_ride(request, ride_id):
    try:
        ride = Ride.objects.get(id=ride_id)
        return Response({
            'ride_id': str(ride.id),
            'status': ride.status,
            'driver_lat': ride.driver_lat,
            'driver_lng': ride.driver_lng,
        })
    except Ride.DoesNotExist:
        return Response({'error': 'Ride not found'}, status=404)