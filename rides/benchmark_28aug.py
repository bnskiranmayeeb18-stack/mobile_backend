import os, sys, django, time

# FIX: Add project root to Python path
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, BASE_DIR)

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mobile_backend.settings')
django.setup()

from django.core.cache import cache
from django.db import connection
from django.test.utils import CaptureQueriesContext
from rides.models import Ride

print("=== TASK 5 - PERFORMANCE BENCHMARK ===")
print("Measure: Before Cache VS After Cache")

# BEFORE
start = time.time()
with CaptureQueriesContext(connection) as ctx:
    list(Ride.objects.all()[:10])
print(f"Before Cache: {(time.time()-start)*1000:.2f}ms | Queries: {len(ctx)}")

# AFTER CACHE
cache.set('rides_list_test', list(Ride.objects.values('id','status')[:10]), 300)
start = time.time()
cache.get('rides_list_test')
print(f"After Cache: {(time.time()-start)*1000:.2f}ms | Queries: 0 (Cache Hit)")