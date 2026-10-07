import os
import sys
from pathlib import Path

# Path fix - bayata unna rides folder ni kuda chudadaniki
current_dir = Path(__file__).resolve().parent
parent_dir = current_dir.parent
sys.path.insert(0, str(parent_dir))
sys.path.insert(0, str(current_dir))

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "settings")

import django

django.setup()

import threading

from django.core.cache import cache

from notifications.models import Notification
from rides.tasks import send_ride_notification

print("\n=== TASK 8 - Duplicate Prevention Test ===\n")

try:
    cache.clear()
except:
    print("Redis lekapoyina parledu - continue...")

Notification.objects.filter(ride_id=101).delete()

ride_id = 101
event = "ride_accepted"
message = "Your ride is accepted"

print(f"Firing SAME event 5 times concurrently for Ride {ride_id}...\n")
results = []


def fire_event(i):
    try:
        result = send_ride_notification.apply(args=[ride_id, event, message]).get()
        results.append(result)
        print(f"Thread-{i}: {result}")
    except Exception as e:
        print(f"Thread-{i} Error: {e}")
        import traceback

        traceback.print_exc()


threads = []
for i in range(1, 6):
    t = threading.Thread(target=fire_event, args=(i,))
    threads.append(t)
    t.start()

for t in threads:
    t.join()

count = Notification.objects.filter(ride_id=ride_id, event_type=event).count()

print("\n--- FINAL DB CHECK ---")
print(f"Total notifications in DB: {count}")
print(f"Expected: 1, Actual: {count} -> {'PASS' if count==1 else 'FAIL'}")
print("\nTask 8 Completed: Duplicate prevention working!" if count == 1 else "\nFAIL")
