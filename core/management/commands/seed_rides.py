import random
from decimal import Decimal
from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from core.models import Ride


class Command(BaseCommand):
    help = 'Task 6 - Generate 3000 rides for Large Dataset'

    def handle(self, *args, **kwargs):
        self.stdout.write("Seeding 3000 rides... Please wait")

        user, _ = User.objects.get_or_create(username='testuser', defaults={'email': 'test@test.com'})
        user.set_password('test123')
        user.save()

        locations = ["Vizag RK Beach", "Gajuwaka", "MVP Colony", "Dwaraka Nagar", "Seethammadhara", "Madhurawada",
                     "Airport", "Railway Station"]
        statuses = ['pending', 'ongoing', 'completed', 'cancelled']
        drivers = [f"Driver_{i}" for i in range(1, 51)]

        Ride.objects.all().delete()  # clean old data
        batch = []
        for i in range(1, 3001):
            batch.append(Ride(
                customer=user,
                pickup_location=random.choice(locations),
                drop_location=random.choice(locations),
                driver_name=random.choice(drivers),
                fare=Decimal(random.randint(50, 1500)),
                status=random.choice(statuses),
            ))
            if len(batch) == 500:
                Ride.objects.bulk_create(batch)
                self.stdout.write(f"  -> {i} rides created...")
                batch = []

        if batch:
            Ride.objects.bulk_create(batch)

        self.stdout.write(self.style.SUCCESS(f"✅ DONE! Total Rides: {Ride.objects.count()}"))