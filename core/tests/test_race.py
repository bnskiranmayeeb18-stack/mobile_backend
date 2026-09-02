import threading
from django.test import TestCase
from django.contrib.auth.models import User
from core.models import Ride
from core.services.ride_service import RideService

class RaceConditionTest(TestCase):
    def test_two_drivers_same_ride(self):
        user = User.objects.create_user('user1')
        driverA = User.objects.create_user('driverA')
        driverB = User.objects.create_user('driverB')
        ride = Ride.objects.create(user=user, pickup_location="A", drop_location="B", status='requested', fare=150, distance_km=8, duration_min=10)

        results = {}

        def driver_a_accept():
            try:
                RideService.accept_ride(ride.id, driverA)
                results['A'] = 'SUCCESS'
            except Exception as e:
                results['A'] = f'REJECTED: {e}'

        def driver_b_accept():
            try:
                RideService.accept_ride(ride.id, driverB)
                results['B'] = 'SUCCESS'
            except Exception as e:
                results['B'] = f'REJECTED: {e}'

        t1 = threading.Thread(target=driver_a_accept)
        t2 = threading.Thread(target=driver_b_accept)
        t1.start()
        t2.start()
        t1.join()
        t2.join()

        print(results)
        # One SUCCESS, one REJECTED
        assert 'SUCCESS' in results.values()
        assert 'REJECTED' in str(results.values()) or list(results.values()).count('SUCCESS') == 1