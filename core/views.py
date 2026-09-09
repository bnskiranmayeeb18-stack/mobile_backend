from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.contrib.auth.models import User
from .models import DriverLocation

# Task 3 - Location Update
@api_view(['POST'])
def update_location(request):
    driver_id = request.data.get('driver_id')
    latitude = request.data.get('latitude')
    longitude = request.data.get('longitude')

    if not driver_id or latitude is None or longitude is None:
        return Response({"error": "driver_id, latitude, longitude required"}, status=400)

    try:
        user = User.objects.get(id=driver_id)
        location, created = DriverLocation.objects.get_or_create(
            driver=user,
            defaults={'latitude': latitude, 'longitude': longitude}
        )
        if not created:
            location.latitude = latitude
            location.longitude = longitude
            location.save()

        return Response({
            "message": "Location updated",
            "driver": user.username,
            "latitude": location.latitude,
            "longitude": location.longitude,
            "is_available": location.is_available
        }, status=200)
    except User.DoesNotExist:
        return Response({"error": "Driver not found"}, status=404)

# Task 4 - Availability Toggle
@api_view(['POST'])
def update_availability(request):
    driver_id = request.data.get('driver_id')
    is_available = request.data.get('is_available')

    if driver_id is None or is_available is None:
        return Response({"error": "driver_id and is_available required"}, status=400)

    try:
        driver_location = DriverLocation.objects.get(driver_id=driver_id)
        driver_location.is_available = bool(is_available)
        driver_location.save()

        return Response({
            "message": "Availability updated",
            "driver": driver_location.driver.username,
            "is_available": driver_location.is_available,
            "last_updated": driver_location.last_updated
        }, status=200)
    except DriverLocation.DoesNotExist:
        return Response({"error": "Driver location not found. Update location first."}, status=404)

# Admin View - For Task 1 proof
@api_view(['GET'])
def admin_driver_locations(request):
    locations = DriverLocation.objects.all()
    data = []
    for loc in locations:
        data.append({
            "driver": loc.driver.username,
            "latitude": loc.latitude,
            "longitude": loc.longitude,
            "is_available": loc.is_available,
            "last_updated": loc.last_updated
        })
    return Response(data, status=200)