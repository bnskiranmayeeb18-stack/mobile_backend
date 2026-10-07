"""
DriverService - Database operations moved from views - Task 3 fix
"""

from django.core.cache import cache


class DriverService:
    @staticmethod
    def find_nearby_drivers(lat, lng, radius_km=5):
        # Database operation + cache moved from views
        cache_key = f"available_drivers_{lat}_{lng}"
        drivers = cache.get(cache_key)
        if drivers:
            return drivers  # HIT

        from drivers.models import Driver

        # Optimized ORM - select_related
        drivers = Driver.objects.select_related("user").filter(
            is_available=True
        )[:10]
        # Cache 60s TTL - business logic
        cache.set(cache_key, list(drivers), timeout=60)
        return drivers

    @staticmethod
    def get_driver_with_cache(driver_id):
        # Database operation moved from views
        cache_key = f"driver_{driver_id}"
        driver = cache.get(cache_key)
        if driver:
            return driver
        from drivers.models import Driver

        driver = Driver.objects.select_related("user").get(id=driver_id)
        cache.set(cache_key, driver, timeout=3600)
        return driver

    @staticmethod
    def invalidate_driver_cache(driver_id):
        cache.delete(f"driver_{driver_id}")
        cache.delete_pattern("available_drivers_*")
