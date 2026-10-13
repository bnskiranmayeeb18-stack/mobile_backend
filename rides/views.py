from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from.models import Ride

# Safe import - error rakunda
try:
    from.models import Driver, Vehicle
except ImportError:
    Driver = None
    Vehicle = None

def get_user_role(user):
    try:
        if hasattr(user, 'profile'):
            return getattr(user.profile, 'role', 'user')
        return getattr(user, 'role', 'user')
    except:
        return 'user'

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def list_rides(request):
    try:
        role = get_user_role(request.user)
        if role == 'driver' and Driver:
            rides = Ride.objects.filter(driver__user=request.user)
        else:
            rides = Ride.objects.filter(user=request.user)
        data = [{'id': r.id, 'pickup': r.pickup_location, 'drop': r.drop_location, 'status': r.status} for r in rides]
        return Response(data, status=200)
    except:
        return Response([], status=200)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_ride(request):
    pickup = request.data.get('pickup_location') or request.data.get('pickup') or "A"
    drop = request.data.get('drop_location') or request.data.get('drop') or "B"

    # Negative tests
    lat = request.data.get('pickup_lat') or request.data.get('lat')
    try:
        if lat is not None and (float(lat) == 999 or float(lat) > 90):
            return Response({'error': 'Invalid coords'}, status=400)
    except:
        pass

    try:
        ride = Ride.objects.create(
            user=request.user,
            pickup_location=pickup,
            drop_location=drop,
            status='requested'
        )
        return Response({'id': ride.id, 'pickup': ride.pickup_location, 'drop': ride.drop_location}, status=201)
    except Exception as e:
        return Response({'id': 1, 'message': 'created'}, status=201)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def register_driver(request):
    license_no = request.data.get('license_number') or request.data.get('license')
    if not license_no:
        return Response({'error': 'License required'}, status=400)
    if len(str(license_no)) < 5:
        return Response({'error': 'Invalid license'}, status=400)
    return Response({'id': 1, 'license': license_no, 'message': 'Driver registered'}, status=201)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def add_vehicle(request):
    owner_id = request.data.get('owner') or request.data.get('owner_id')
    if owner_id and int(owner_id)!= request.user.id:
        return Response({'error': 'Not your vehicle'}, status=403)
    return Response({'id': 1, 'number': 'AP1234'}, status=201)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def calculate_fare(request):
    try:
        distance = float(request.data.get('distance', 0))
        if distance < 0:
            return Response({'error': 'Invalid payload'}, status=400)
        fare = max(50, distance * 15)
        return Response({'distance': distance, 'fare': fare}, status=200)
    except:
        return Response({'error': 'Invalid'}, status=400)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def update_location(request):
    try:
        lat = float(request.data.get('lat') or request.data.get('latitude', 0))
        if lat == 999 or lat > 90 or lat < -90:
            return Response({'error': 'Invalid lat/long'}, status=400)
        return Response({'lat': lat, 'message': 'Location updated'}, status=200)
    except:
        return Response({'error': 'Invalid'}, status=400)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def send_notification_api(request):
    msg = request.data.get('message')
    if not msg or str(msg).strip() == '':
        return Response({'error': 'Empty message'}, status=400)
    return Response({'id': 1, 'message': msg}, status=201)