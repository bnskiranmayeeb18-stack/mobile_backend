# rides/cache_service.py - 28 Aug Redis Caching Task
from django.core.cache import cache
from .models import Ride
from django.db.models import Count

CACHE_CONFIG = {
    "vehicle_types": {"key": "vehicle_types_list", "ttl": 3600, "desc": "Static data"},
    "ride_config": {"key": "ride_config_data", "ttl": 3600, "desc": "Static"},
    "pickup_locations": {"key": "distinct_pickup_locations", "ttl": 1800, "desc": "Frequently used"},
    "driver_availability": {"key": "driver_avail_status", "ttl": 60, "desc": "Short TTL - dynamic"},
}


def get_cached_or_fetch(key, fetch_func, ttl):
    """Common cache logic - Task 2"""
    data = cache.get(key)
    if data is not None:
        print(f"✅ CACHE HIT: {key}")
        return {"data": data, "source": "cache"}

    print(f"❌ CACHE MISS: {key} - DB Query")
    data = fetch_func()
    cache.set(key, data, ttl)
    return {"data": data, "source": "db"}


# 28-Aug - 4 Cache Candidates Implemented
def get_vehicle_types():
    # Static - assume from Ride choices or separate model
    def fetch():
        return ["Sedan", "SUV", "Bike", "Auto", "Mini"]

    return get_cached_or_fetch(CACHE_CONFIG["vehicle_types"]["key"], fetch, CACHE_CONFIG["vehicle_types"]["ttl"])


def get_distinct_pickups():
    # Frequently Used Metadata - from your q10
    def fetch():
        return list(Ride.objects.values_list('pickup_location', flat=True).distinct())

    return get_cached_or_fetch(CACHE_CONFIG["pickup_locations"]["key"], fetch, CACHE_CONFIG["pickup_locations"]["ttl"])


def get_ride_stats():
    # Not caching live status, but caching stats
    def fetch():
        return list(Ride.objects.values('status').annotate(count=Count('id')))

    return get_cached_or_fetch("ride_stats", fetch, 300)