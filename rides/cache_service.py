from django.core.cache import cache

def invalidate_ride_cache():
    try:
        # Redis ki
        cache.delete_pattern("rides_list_page_*")
        cache.delete_pattern("ride_detail_*")
    except:
        # LocMemCache ki (dev)
        cache.clear()
    print("Cache Invalidated")