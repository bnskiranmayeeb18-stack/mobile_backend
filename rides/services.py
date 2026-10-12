import math, logging
from django.core.cache import cache
from .models import DriverProfile, Ride
from django.db.models import F
from django.db import transaction

logger = logging.getLogger('api')


def haversine(lat1, lon1, lat2, lon2):
    R = 6371
    dlat = math.radians(lat2 - lat1)
    dlon = math.radians(lon2 - lon1)
    a = math.sin(dlat / 2) ** 2 + math.cos(math.radians(lat1)) * math.cos(math.radians(lat2)) * math.sin(dlon / 2) ** 2
    return R * 2 * math.asin(math.sqrt(a))


def find_nearby_drivers(pickup_lat, pickup_lng, radius_km=5):
    cache_key = f"drivers_online_{pickup_lat:.2f}_{pickup_lng:.2f}"
    cached = cache.get(cache_key)
    if cached is not None:
        logger.info(f"CACHE HIT {cache_key}")
        return cached

    logger.info(f"CACHE MISS {cache_key}")
    drivers = DriverProfile.objects.filter(is_online=True, current_lat__isnull=False).exclude(current_lat=0)
    eligible = []
    for d in drivers:
        dist = haversine(pickup_lat, pickup_lng, d.current_lat, d.current_lng)
        if dist <= radius_km:
            eligible.append({"driver_id": d.user_id, "distance_km": round(dist, 2), "profile": d})
    eligible.sort(key=lambda x: x['distance_km'])

    cache.set(cache_key, eligible, 30)  # 30 sec cache
    return eligible


@transaction.atomic
def accept_ride_safe(ride_id, driver_user):
    # Optimistic locking for concurrent acceptance
    ride = Ride.objects.select_for_update().get(id=ride_id)
    if ride.status != 'REQUESTED':
        raise ValueError(f"Ride already {ride.status}")
    ride.driver = driver_user
    ride.status = 'ACCEPTED'
    ride.version = F('version') + 1
    ride.save()
    # Invalidate cache
    cache.delete_pattern("drivers_online_*")
    return ride