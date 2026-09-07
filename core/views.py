from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from rest_framework.authtoken.models import Token
from rest_framework.generics import ListAPIView
from django.db.models import Q
from.models import Ride
from.serializers import RideSerializer

# Constants for status validation
INVALID_TRANSITIONS = {
    ('COMPLETED', 'STARTED'),
    ('COMPLETED', 'CANCELLED'),
}

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
    ride = Ride.objects.create(
        user=request.user,
        customer=request.user,
        status='REQUESTED'
    )
    return Response({"id": ride.id, "status": ride.status}, status=201)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def ride_detail(request, ride_id):
    try:
        ride = Ride.objects.select_related('customer').get(id=ride_id)
    except Ride.DoesNotExist:
        return Response({"error": "Ride not found"}, status=404)

    # Security: only owner can view
    if ride.customer!= request.user:
        return Response({"error": "Permission denied"}, status=403)

    return Response({
        "id": ride.id,
        "customer": ride.customer.username if ride.customer else None,
        "status": ride.status
    }, status=200)

@api_view(['PATCH'])
@permission_classes([IsAuthenticated])
def ride_status_update(request, ride_id):
    try:
        ride = Ride.objects.get(id=ride_id)
    except Ride.DoesNotExist:
        return Response({"error": "Ride not found"}, status=404)

    new_status = request.data.get('status')
    if not new_status:
        return Response({"error": "status field required"}, status=400)

    old_status = ride.status

    # Validation logic in service style
    if old_status == 'CANCELLED':
        return Response({"error": "Cannot transition from CANCELLED"}, status=400)

    if (old_status, new_status) in INVALID_TRANSITIONS:
        return Response(
            {"error": f"Cannot transition {old_status}->{new_status}"},
            status=400
        )

    ride.status = new_status
    ride.save()

    return Response({
        "id": ride.id,
        "old_status": old_status,
        "new_status": ride.status
    }, status=200)


def apply_ride_filters(queryset, request):
    date = request.query_params.get('date')  # ?date=2025-09-07
    status = request.query_params.get('status')  # ?status=COMPLETED
    driver = request.query_params.get('driver')  # ?driver=1
    fare_min = request.query_params.get('fare_min')
    fare_max = request.query_params.get('fare_max')

    if date:
        queryset = queryset.filter(created_at__date=date)
    if status:
        queryset = queryset.filter(status=status)
    if driver:
        queryset = queryset.filter(driver_id=driver)
    if fare_min:
        queryset = queryset.filter(fare__gte=fare_min)
    if fare_max:
        queryset = queryset.filter(fare__lte=fare_max)

    return queryset.select_related('customer', 'driver').order_by('-created_at')


# 1. GET /api/rides/history/ - anni rides
class RideHistoryView(ListAPIView):
    serializer_class = RideSerializer

    def get_queryset(self):
        qs = Ride.objects.all()
        return apply_ride_filters(qs, self.request)


# 2. GET /api/rides/active/ - REQUESTED, ACCEPTED, STARTED
class RideActiveView(ListAPIView):
    serializer_class = RideSerializer

    def get_queryset(self):
        qs = Ride.objects.filter(status__in=['REQUESTED', 'ACCEPTED', 'STARTED'])
        return apply_ride_filters(qs, self.request)


# 3. GET /api/rides/completed/
class RideCompletedView(ListAPIView):
    serializer_class = RideSerializer

    def get_queryset(self):
        qs = Ride.objects.filter(status='COMPLETED')
        return apply_ride_filters(qs, self.request)


# 4. GET /api/rides/cancelled/
class RideCancelledView(ListAPIView):
    serializer_class = RideSerializer

    def get_queryset(self):
        qs = Ride.objects.filter(status='CANCELLED')
        return apply_ride_filters(qs, self.request)