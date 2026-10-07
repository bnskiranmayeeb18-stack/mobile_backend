# rides/cache_service.py - 28 Aug FIXED
import os
import sys

import django

# Django setup - FIRST LINE lo undali
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "mobile_backend.settings")
django.setup()

# Tarvata imports
from django.core.cache import cache
from django.db.models import Count

from rides.models import Ride

CACHE_CONFIG = {
    "vehicle_types": {"key": "vehicle_types_list", "ttl": 3600},
    "pickup_locations": {"key": "distinct_pickup_locations", "ttl": 1800},
}


def get_cached_or_fetch(key, fetch_func, ttl):
    data = cache.get(key)
    if data is not None:
        print(f"✅ CACHE HIT: {key}")
        return {"data": data, "source": "cache"}
    print(f"❌ CACHE MISS: {key} - DB Query")
    data = fetch_func()
    cache.set(key, data, ttl)
    return {"data": data, "source": "db"}


def get_vehicle_types():
    def fetch():
        return ["Sedan", "SUV", "Bike", "Auto", "Mini"]

    return get_cached_or_fetch(
        CACHE_CONFIG["vehicle_types"]["key"],
        fetch,
        CACHE_CONFIG["vehicle_types"]["ttl"],
    )


def get_distinct_pickups():
    def fetch():
        return list(Ride.objects.values_list("pickup_location", flat=True).distinct())

    return get_cached_or_fetch(
        CACHE_CONFIG["pickup_locations"]["key"],
        fetch,
        CACHE_CONFIG["pickup_locations"]["ttl"],
    )


# Test
if __name__ == "__main__":
    print("=== 28-Aug Redis Caching Test ===")
    r1 = get_vehicle_types()
    print(f"Call 1: {r1['source']} -> {r1['data']}")
    r2 = get_vehicle_types()
    print(f"Call 2: {r2['source']} -> {r2['data']}")

    r3 = get_distinct_pickups()
    print(f"Pickup: {r3['source']} -> {r3['data']}")

    print("\n✅ PASS if 1st=db, 2nd=cache")
    from django.core.cache import cache

    # Task 4 - Cache Invalidation - Stale data rakunda
    def invalidate_driver_cache(driver_id):
        """Driver status update ayyaka cache delete chesi kotha data store cheyyadam"""
        print(f"\n[Task 4] Driver {driver_id} Status Updated!")

        # Step 1: Invalidate Cache
        cache.delete("driver_availability")
        cache.delete(f"driver_{driver_id}_status")
        print(f"  -> Step 1: Invalidate Cache DONE (deleted driver_{driver_id}_status)")

        # Step 2: Store Updated Data
        updated_data = {
            "driver_id": driver_id,
            "status": "AVAILABLE",
            "location": "Vizag MVP",
            "updated_at": "28-Aug-2026 2:45 PM",
        }
        cache.set(f"driver_{driver_id}_status", updated_data, timeout=60)
        print(f"  -> Step 2: Store Updated Data DONE: {updated_data}")
        print("  ✅ Stale data radu - Fresh data only!")
        return updated_data

    def get_driver_status(driver_id):
        key = f"driver_{driver_id}_status"
        data = cache.get(key)
        if data:
            print(f"  ✅ CACHE HIT: {data} (No stale data)")
            return data
        else:
            print(f"  ❌ CACHE MISS - DB nundi teesukovali")
            return None
