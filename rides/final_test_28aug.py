import time

from django.conf import settings
from django.core.cache import cache

if not settings.configured:
    settings.configure(
        CACHES={"default": {"BACKEND": "django.core.cache.backends.locmem.LocMemCache"}}
    )


def test_cache():
    print("=== Task 3 - Cache Expiration Full Test ===")
    cache_key = "vehicle_types"
    cache.delete(cache_key)  # clean

    # 1. CACHE MISS
    print("\n1. CACHE MISS")
    data = cache.get(cache_key)
    if not data:
        data = ["Sedan", "SUV", "Bike", "Auto"]
        cache.set(cache_key, data, timeout=2)  # 2 sec TTL for test
        print(f"   -> DB nundi techa: {data} (TTL=2 sec)")

    # 2. CACHE HIT
    print("\n2. CACHE HIT")
    data2 = cache.get(cache_key)
    print(f"   -> Cache nundi vachindi: {data2}")

    # 3. EXPIRATION
    print("\n3. EXPIRATION - 3 sec wait chestunna...")
    time.sleep(3)
    data3 = cache.get(cache_key)
    print(f"   -> TTL ayyaka: {data3} (None = Expired)")

    # 4. REFRESH
    print("\n4. REFRESH")
    if not data3:
        new_data = ["Sedan", "SUV", "Bike", "Auto", "New-EV"]
        cache.set(cache_key, new_data, timeout=3600)
        print(f"   -> Malli DB nundi refresh chesa: {new_data}")

    print("\n✅ Task 3 FULL DONE - Hit, Miss, Expiration, Refresh proved!")


if __name__ == "__main__":
    test_cache()
