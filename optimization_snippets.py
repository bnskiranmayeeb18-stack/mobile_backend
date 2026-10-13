from django.core.cache import cache
from rest_framework.pagination import PageNumberPagination
from django.db.models import Prefetch

class StandardPagination(PageNumberPagination):
    page_size = 20
    page_size_query_param = 'page_size'
    max_page_size = 100

# Booking history - optimized
# Before: Booking.objects.all() -> N+1
# After:
# bookings = Booking.objects.select_related('customer', 'provider').prefetch_related('payments').filter(customer=request.user)

# Cache example
def get_cached_services():
    key = "services_list"
    data = cache.get(key)
    if data:
        return data, True  # hit
    data = list(Service.objects.all())  # query
    cache.set(key, data, 300)  # TTL 5min
    return data, False  # miss
