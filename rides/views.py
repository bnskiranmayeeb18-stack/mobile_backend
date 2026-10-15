from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.utils import timezone
from django.utils.dateparse import parse_datetime
from django.db import models
import base64, json
from.models import Ride
from.serializers import RideSerializer

def _create_ride(request):
    serializer = RideSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save(rider=request.user)
        return Response(serializer.data, status=201)
    return Response(serializer.errors, status=400)

@api_view(["GET","POST"])
@permission_classes([IsAuthenticated])
def ride_list_create(request):
    if request.method == "GET":
        return list_rides(request)
    return _create_ride(request)

@api_view(["POST"])
@permission_classes([IsAuthenticated])
def create_ride(request):
    return _create_ride(request)

@api_view(["POST"])
@permission_classes([IsAuthenticated])
def ride_create(request):
    return _create_ride(request)

# --- Core Logic WITHOUT api_view to avoid double wrap ---
def _do_accept(ride_id, user):
    ride = Ride.objects.get(id=ride_id)
    ride.status = "accepted"
    ride.driver = user
    ride.save()
    return ride

def _do_start(ride_id, user):
    ride = Ride.objects.get(id=ride_id)
    if ride.rider!= user and ride.driver!= user and not user.is_staff:
        return None
    if ride.status == "started":
        return ride
    ride.status = "started"
    ride.save()
    return ride

def _do_complete(ride_id, user):
    ride = Ride.objects.get(id=ride_id)
    if ride.rider!= user and ride.driver!= user and not user.is_staff:
        return None
    ride.status = "completed"
    ride.save()
    return ride

def _do_cancel(ride_id, user):
    ride = Ride.objects.get(id=ride_id)
    if ride.rider!= user and not user.is_staff:
        return None
    ride.status = "cancelled"
    ride.save()
    return ride

# --- API Views - Each endpoint has its OWN logic, no cross-calling ---
@api_view(["POST"])
@permission_classes([IsAuthenticated])
def ride_accept(request, pk=None, ride_id=None):
    _id = ride_id or pk
    try:
        ride = _do_accept(_id, request.user)
        return Response(RideSerializer(ride).data)
    except Ride.DoesNotExist:
        return Response(status=404)

@api_view(["POST"])
@permission_classes([IsAuthenticated])
def accept_ride(request, ride_id=None, pk=None):
    _id = ride_id or pk
    try:
        ride = _do_accept(_id, request.user)
        return Response(RideSerializer(ride).data)
    except Ride.DoesNotExist:
        return Response(status=404)

@api_view(["POST"])
@permission_classes([IsAuthenticated])
def ride_start(request, pk=None, ride_id=None):
    _id = ride_id or pk
    try:
        ride = _do_start(_id, request.user)
        if ride is None:
            return Response(status=404)
        return Response(RideSerializer(ride).data)
    except Ride.DoesNotExist:
        return Response(status=404)

@api_view(["POST"])
@permission_classes([IsAuthenticated])
def start_ride(request, ride_id=None, pk=None):
    _id = ride_id or pk
    try:
        ride = _do_start(_id, request.user)
        if ride is None:
            return Response(status=404)
        return Response(RideSerializer(ride).data)
    except Ride.DoesNotExist:
        return Response(status=404)

@api_view(["POST"])
@permission_classes([IsAuthenticated])
def ride_complete(request, pk=None, ride_id=None):
    _id = ride_id or pk
    try:
        ride = _do_complete(_id, request.user)
        if ride is None:
            return Response(status=404)
        return Response(RideSerializer(ride).data)
    except Ride.DoesNotExist:
        return Response(status=404)

@api_view(["POST"])
@permission_classes([IsAuthenticated])
def complete_ride(request, ride_id=None, pk=None):
    _id = ride_id or pk
    try:
        ride = _do_complete(_id, request.user)
        if ride is None:
            return Response(status=404)
        return Response(RideSerializer(ride).data)
    except Ride.DoesNotExist:
        return Response(status=404)

@api_view(["POST"])
@permission_classes([IsAuthenticated])
def ride_cancel(request, pk=None, ride_id=None):
    _id = ride_id or pk
    try:
        ride = _do_cancel(_id, request.user)
        if ride is None:
            return Response(status=404)
        return Response(RideSerializer(ride).data)
    except Ride.DoesNotExist:
        return Response(status=404)

@api_view(["POST"])
@permission_classes([IsAuthenticated])
def cancel_ride(request, ride_id=None, pk=None):
    _id = ride_id or pk
    try:
        ride = _do_cancel(_id, request.user)
        if ride is None:
            return Response(status=404)
        return Response(RideSerializer(ride).data)
    except Ride.DoesNotExist:
        return Response(status=404)

@api_view(["GET"])
@permission_classes([IsAuthenticated])
def get_ride(request, ride_id=None, pk=None):
    _id = ride_id or pk
    try:
        ride = Ride.objects.get(id=_id)
        if ride.rider!= request.user and ride.driver!= request.user and not request.user.is_staff:
            return Response(status=404)
        return Response(RideSerializer(ride).data)
    except Ride.DoesNotExist:
        return Response(status=404)

@api_view(["GET"])
@permission_classes([IsAuthenticated])
def list_rides(request):
    rides = Ride.objects.all()
    if not request.user.is_staff:
        rides = rides.filter(models.Q(rider=request.user) | models.Q(driver=request.user))
    rides = rides.order_by("-updated_at","-id")
    return Response(RideSerializer(rides, many=True).data)

# Offline Sync
def encode_cursor(updated_at, pk):
    payload = json.dumps({"updated_at": updated_at.isoformat(), "id": pk})
    return base64.urlsafe_b64encode(payload.encode()).decode()

def decode_cursor(cursor_str):
    try:
        data = json.loads(base64.urlsafe_b64decode(cursor_str.encode()).decode())
        return parse_datetime(data["updated_at"]), data["id"]
    except Exception:
        return None, None

@api_view(["GET"])
@permission_classes([IsAuthenticated])
def ride_sync(request):
    qs = Ride.objects.filter(models.Q(rider=request.user) | models.Q(driver=request.user)).order_by("-updated_at","-id")
    updated_since = request.GET.get("updated_since")
    if updated_since:
        dt = parse_datetime(updated_since)
        if dt:
            qs = qs.filter(updated_at__gt=dt)
    cursor = request.GET.get("cursor")
    if cursor:
        dt, pk = decode_cursor(cursor)
        if dt:
            qs = qs.filter(models.Q(updated_at__lt=dt) | models.Q(updated_at=dt, id__lt=pk))
    limit = min(int(request.GET.get("limit", 20)), 100)
    items = list(qs[:limit+1])
    has_more = len(items) > limit
    items = items[:limit]
    next_cursor = None
    if has_more and items:
        last = items[-1]
        next_cursor = encode_cursor(last.updated_at, last.id)
    ser = RideSerializer(items, many=True)
    return Response({
        "items": ser.data,
        "next_cursor": next_cursor,
        "has_more": has_more,
        "sync_token": timezone.now().isoformat(),
        "count": len(ser.data)
    })
