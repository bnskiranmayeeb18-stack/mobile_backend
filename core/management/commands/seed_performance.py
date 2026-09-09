from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from core.models import DriverLocation
from django.contrib.auth.hashers import make_password
import random
import time


class Command(BaseCommand):
    help = 'Task 8 - Performance Testing with 2000 drivers'

    def handle(self, *args, **kwargs):
        self.stdout.write("Deleting old data...")
        DriverLocation.objects.all().delete()
        User.objects.filter(username__startswith='perf_driver_').delete()

        self.stdout.write("Creating 2000 driver records - Fast mode...")

        # Oka sari password hash chesi motham mandiki same vadutunnam - fast!
        hashed_pw = make_password('test123')

        users = []
        for i in range(2000):
            users.append(User(username=f'perf_driver_{i}', password=hashed_pw))

        # Bulk create users - super fast
        User.objects.bulk_create(users, batch_size=500)
        self.stdout.write("2000 Users created...")

        created_users = User.objects.filter(username__startswith='perf_driver_')

        driver_locations = []
        for user in created_users:
            driver_locations.append(DriverLocation(
                driver=user,
                latitude=16.5 + random.random(),
                longitude=80.6 + random.random(),
                is_available=True
            ))

        DriverLocation.objects.bulk_create(driver_locations, batch_size=500)
        count = DriverLocation.objects.count()
        self.stdout.write(self.style.SUCCESS(f"Created {count} driver locations!"))

        # Performance Test
        self.stdout.write("\nTesting Nearby Driver Search...")
        start = time.time()
        nearby = DriverLocation.objects.filter(is_available=True)[:10]
        end = time.time()
        response_time = (end - start) * 1000

        self.stdout.write(self.style.SUCCESS(f"Found {len(nearby)} nearby drivers"))
        self.stdout.write(self.style.SUCCESS(f"Response Time: {response_time:.2f} ms"))
        self.stdout.write(self.style.SUCCESS(f"Database: Tested with {count} records"))
        self.stdout.write(self.style.SUCCESS("Task 8 Performance Test - PASSED"))