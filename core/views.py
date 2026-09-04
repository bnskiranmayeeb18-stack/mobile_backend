from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from rest_framework.authtoken.models import Token
from.models import Ride

@api_view(['POST'])
@permission_classes([AllowAny])
def register_customer(request):
    username = request.data.get('username')
    password = request.data.get('password')
    email = request.data.get('email', '')
    if not username or not password:
        return Response({"error": "username and password required"}, status=400)
    if User.objects.filter(username=username).exists():
        return Response({"error": "user already exists"}, status=400)
    user = User.objects.create_user(username=username, password=password, email=email)
    return Response({"id": user.id, "username": user.username}, status=201)

@api_view(['POST'])
@permission_classes([AllowAny])
def login_view(request):
    username = request.data.get('username')
    password = request.data.get('password')
    if not username or not password:
        return Response({"error": "username and password required"}, status=400)
    user = authenticate(username=username, password=password)
    if not user:
        return Response({"error": "invalid credentials"}, status=400)
    token, _ = Token.objects.get_or_create(user=user)
    return Response({"token": token.key}, status=200)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_ride(request):
    user = request.user
    ride = Ride.objects.create(user=user, customer=user, status='REQUESTED')
    return Response({"id": ride.id, "status": ride.status}, status=201)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def ride_detail(request, ride_id):
    try:
        ride = Ride.objects.get(id=ride_id)
    except Ride.DoesNotExist:
        return Response({"error": "Ride not found"}, status=404)
    return Response({"id": ride.id, "customer": ride.customer.username if ride.customer else None, "status": ride.status}, status=200)

@api_view(['PATCH'])
@permission_classes([IsAuthenticated])
def ride_status_update(request, ride_id):
    try:
        ride = Ride.objects.get(id=ride_id)
    except Ride.DoesNotExist:
        return Response({"error": "Ride not found"}, status=404)
    new_status = request.data.get('status')
    old_status = ride.status
    if old_status == 'COMPLETED' and new_status == 'STARTED':
        return Response({"error": "Cannot transition COMPLETED->STARTED"}, status=400)
    if old_status == 'CANCELLED':
        return Response({"error": "Cannot transition from CANCELLED"}, status=400)
    if old_status == 'COMPLETED' and new_status == 'CANCELLED':
        return Response({"error": "Cannot cancel completed ride"}, status=400)
    ride.status = new_status
    ride.save()
    return Response({"id": ride.id, "old_status": old_status, "new_status": ride.status}, status=200)