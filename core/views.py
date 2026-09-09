import math
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import DriverLocation


# Haversine function - Task 6
def haversine(lat1, lon1, lat2, lon2):
    R = 6371  # Earth radius in km
    d_lat = math.radians(lat2 - lat1)
    d_lon = math.radians(lon2 - lon1)
    a = math.sin(d_lat / 2) ** 2 + math.cos(math.radians(lat1)) * math.cos(math.radians(lat2)) * math.sin(
        d_lon / 2) ** 2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    return R * c


# Task 3 - Location Update
class DriverLocationUpdateView(APIView):
    def post(self, request):
        driver_id = request.data.get('driver_id')
        lat = request.data.get('latitude')
        lon = request.data.get('longitude')

        if not driver_id or lat is None or lon is None:
            return Response({"error": "Missing coordinates"}, status=400)

        try:
            lat = float(lat)
            lon = float(lon)
            # Task 7 validation
            if not (-90 <= lat <= 90) or not (-180 <= lon <= 180):
                return Response({"error": "Invalid latitude or longitude"}, status=400)
        except:
            return Response({"error": "Invalid latitude"}, status=400)

        obj, _ = DriverLocation.objects.update_or_create(
            driver_id=driver_id,
            defaults={'latitude': lat, 'longitude': lon}
        )
        return Response({"message": "Location updated"}, status=200)


# Task 4 - Availability Toggle
class DriverAvailabilityView(APIView):
    def post(self, request):
        driver_id = request.data.get('driver_id')
        is_available = request.data.get('is_available')

        if driver_id is None or is_available is None:
            return Response({"error": "Missing fields"}, status=400)

        try:
            driver = DriverLocation.objects.get(driver_id=driver_id)
            # Task 7 - reject offline/busy check
            if driver.is_available == False and is_available == True:
                pass  # allow coming online
            driver.is_available = bool(is_available)
            driver.save()
            return Response({"driver_id": str(driver_id), "is_available": driver.is_available}, status=200)
        except DriverLocation.DoesNotExist:
            return Response({"error": "Offline drivers"}, status=404)


# Task 5 & 6 - Nearby Driver with Distance Calculation + Sort
class NearbyDriverView(APIView):
    def get(self, request):
        try:
            user_lat = float(request.query_params.get('latitude'))
            user_lon = float(request.query_params.get('longitude'))
            radius = float(request.query_params.get('radius', 10))
        except:
            return Response({"error": "Missing coordinates or Invalid radius"}, status=400)

        # Task 7 validation
        if not (-90 <= user_lat <= 90) or not (-180 <= user_lon <= 180):
            return Response({"error": "Invalid latitude or longitude"}, status=400)
        if radius <= 0 or radius > 100:
            return Response({"error": "Invalid radius"}, status=400)

        available_drivers = DriverLocation.objects.filter(is_available=True)
        result = []

        for driver in available_drivers:
            # Skip drivers with no location
            if driver.latitude is None or driver.longitude is None:
                continue

            dist = haversine(user_lat, user_lon, driver.latitude, driver.longitude)

            if dist <= radius:
                result.append({
                    "driver_id": str(driver.driver_id),
                    "distance_km": round(dist, 1)  # Task 6 format 1.7
                })

        # Task 6 - Sort drivers by nearest distance
        result_sorted = sorted(result, key=lambda x: x['distance_km'])

        return Response(result_sorted, status=200)