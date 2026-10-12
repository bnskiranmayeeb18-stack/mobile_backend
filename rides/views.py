from rest_framework import status, permissions
from rest_framework.views import APIView
from rest_framework.response import Response
from django.core.cache import cache
from .models import Ride, DriverProfile
from .serializers import RideCreateSerializer, RideSerializer, DriverLocationSerializer
from .services import find_nearby_drivers, accept_ride_safe
from .tasks import notify_drivers_task, notify_passenger_task
import logging

logger = logging.getLogger('api')

class RideCreateView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    def post(self, request):
        ser = RideCreateSerializer(data=request.data, context={'request':request})
        ser.is_valid(raise_exception=True)
        ride = ser.save(passenger=request.user, status='REQUESTED')
        # Driver matching
        drivers = find_nearby_drivers(ride.pickup_lat, ride.pickup_lng)
        # Async notify
        notify_drivers_task.delay(ride.id, drivers[:5])
        logger.info(f"Ride {ride.id} created, found {len(drivers)} drivers")
        return Response({"success":True,"data":RideSerializer(ride).data,"eligible_drivers":drivers[:5]}, status=201)

class RideAcceptView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    def post(self, request, ride_id):
        try:
            ride = accept_ride_safe(ride_id, request.user)
            notify_passenger_task.delay(ride.id, "ACCEPTED")
            # WebSocket notify via cache/channel
            return Response({"success":True,"data":RideSerializer(ride).data})
        except Ride.DoesNotExist:
            return Response({"success":False,"message":"Ride not found","error_code":"RIDE_NOT_FOUND"}, status=404)
        except ValueError as e:
            return Response({"success":False,"message":str(e),"error_code":"RIDE_ALREADY_ACCEPTED"}, status=409)

class RideStatusView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    def patch(self, request, ride_id):
        event = request.data.get('status')  # STARTED, COMPLETED
        ride = Ride.objects.get(id=ride_id, passenger=request.user)
        if event in ['STARTED','COMPLETED']:
            ride.status = event
            ride.save()
            notify_passenger_task.delay(ride.id, event)
        return Response({"success":True,"data":RideSerializer(ride).data})

class DriverLocationView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    def post(self, request):
        profile, _ = DriverProfile.objects.get_or_create(user=request.user)
        ser = DriverLocationSerializer(profile, data=request.data, partial=True)
        ser.is_valid(raise_exception=True)
        ser.save()
        cache.set(f"driver_loc_{request.user.id}", ser.data, 60)
        return Response({"success":True,"data":ser.data})

class DriverOnlineView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    def post(self, request):
        profile, _ = DriverProfile.objects.get_or_create(user=request.user)
        profile.is_online = request.data.get('is_online', True)
        profile.save()
        return Response({"success":True,"is_online":profile.is_online})