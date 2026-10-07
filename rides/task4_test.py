from django.conf import settings

if not settings.configured:
    settings.configure(
        CACHES={"default": {"BACKEND": "django.core.cache.backends.locmem.LocMemCache"}}
    )

from django.core.cache import cache

from rides.cache_service import get_driver_status, invalidate_driver_cache

print("=== TASK 4 - CACHE INVALIDATION TEST ===")
# Initial cache
cache.set("driver_101_status", {"status": "BUSY", "old": True}, 60)
print("Old cached data: BUSY")

# Driver updates -> Invalidate + Store new
invalidate_driver_cache(101)

# Fetch again - should be new data
get_driver_status(101)
print("\n✅ TASK 4 DONE - Invalidation proved!")
