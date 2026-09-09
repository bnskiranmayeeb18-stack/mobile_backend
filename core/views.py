import json
import math
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.models import User
from .models import DriverLocation


def haversine(lat1, lon1, lat2, lon2):
    R = 6371
    dlat = math.radians(lat2 - lat1)
    dlon = math.radians(lon2 - lon1)
    a = math.sin(dlat / 2) ** 2 + math.cos(math.radians(lat1)) * math.cos(math.radians(lat2)) * math.sin(dlon / 2) ** 2
    return R * 2 * math.asin(math.sqrt(a))


@csrf_exempt
def location_update(request):
    if request.method != 'POST':
        return JsonResponse({"error": "POST only"}, status=405)
    try:
        data = json.loads(request.body)
    except:
        return JsonResponse({"error": "Invalid JSON"}, status=400)

    driver_id = data.get('driver_id')
    lat = data.get('latitude')
    lng = data.get('longitude')

    # Task 7 Validation
    if driver_id is None or lat is None or lng is None:
        return JsonResponse({"error": "Missing coordinates or driver_id"}, status=400)
    try:
        lat = float(lat)
        lng = float(lng)
        driver_id = int(driver_id)
    except:
        return JsonResponse({"error": "Invalid latitude or longitude"}, status=400)

    if not (-90 <= lat <= 90):
        return JsonResponse({"error": "Invalid latitude - must be between -90 and 90"}, status=400)
    if not (-180 <= lng <= 180):
        return JsonResponse({"error": "Invalid longitude - must be between -180 and 180"}, status=400)

    try:
        user = User.objects.get(id=driver_id)
        # get_or_create - first time location update ki
        loc, created = DriverLocation.objects.get_or_create(driver=user)
        loc.latitude = lat
        loc.longitude = lng
        loc.save()
        return JsonResponse({"message": "Location updated", "driver_id": driver_id}, status=200)
    except User.DoesNotExist:
        return JsonResponse({"error": "Driver not found"}, status=404)


@csrf_exempt
def availability(request):
    if request.method != 'POST':
        return JsonResponse({"error": "POST only"}, status=405)
    try:
        data = json.loads(request.body)
    except:
        return JsonResponse({"error": "Invalid JSON"}, status=400)

    driver_id = data.get('driver_id')
    is_available = data.get('is_available')

    if driver_id is None or is_available is None:
        return JsonResponse({"error": "Missing driver_id or is_available"}, status=400)

    try:
        user = User.objects.get(id=int(driver_id))
        loc, created = DriverLocation.objects.get_or_create(driver=user)
        loc.is_available = bool(is_available)
        loc.save()
        return JsonResponse({"driver_id": str(user.id), "is_available": loc.is_available}, status=200)
    except User.DoesNotExist:
        return JsonResponse({"error": "Driver not found"}, status=404)


def nearby(request):
    lat = request.GET.get('latitude')
    lng = request.GET.get('longitude')
    radius = request.GET.get('radius')

    if not lat or not lng:
        return JsonResponse({"error": "Missing coordinates"}, status=400)
    if not radius:
        return JsonResponse({"error": "Missing radius"}, status=400)

    try:
        lat = float(lat)
        lng = float(lng)
        radius = float(radius)
    except:
        return JsonResponse({"error": "Invalid latitude, longitude or radius"}, status=400)

    if not (-90 <= lat <= 90):
        return JsonResponse({"error": "Invalid latitude"}, status=400)
    if not (-180 <= lng <= 180):
        return JsonResponse({"error": "Invalid longitude"}, status=400)
    if radius <= 0 or radius > 100:
        return JsonResponse({"error": "Invalid radius - must be >0 and <=100 km"}, status=400)

    # Task 7: Reject Offline drivers -> is_available=True only
    # Note: is_busy field nee model lo ledu, so only is_available filter
    drivers = DriverLocation.objects.filter(is_available=True)

    result = []
    for d in drivers:
        dist = haversine(lat, lng, d.latitude, d.longitude)
        if dist <= radius:
            result.append({"driver_id": str(d.driver.id), "distance_km": round(dist, 2)})

    result.sort(key=lambda x: x['distance_km'])
    return JsonResponse(result, safe=False, status=200)