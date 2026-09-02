from django.test import TestCase
from core.models import Ride, DriverProfile, Vehicle
from core.services.fare_service import FareService
from core.services.ride_service import RideService

class TestBusinessLogic(TestCase):
    def setUp(self):
        v1 = Vehicle.objects.create(registration_number="AP31-1234")
        v2 = Vehicle.objects.create(registration_number="AP31-5678")
        self.driver1 = DriverProfile.objects.create(name="Driver1", vehicle=v1, is_active=True)
        self.driver2 = DriverProfile.objects.create(name="Driver2", vehicle=v2, is_active=True)

    # 1. Fare calculation
    def test_fare_calculation(self):
        fare = FareService.get_fare_estimate(8, 10)
        self.assertEqual(fare, 150) # 40+80+20+10

    # 2. Ride creation
    def test_ride_creation(self):
        ride = RideService.create_ride("Kiranmayee", "Ameerpet", "Gachibowli", 8, 10)
        self.assertEqual(ride.status, 'REQUESTED')
        self.assertEqual(ride.fare, 150)
        self.assertEqual(ride.customer_name, "Kiranmayee")

    # 3. Ride acceptance
    def test_ride_acceptance(self):
        ride = RideService.create_ride("Kiranmayee", "A", "B", 5, 5)
        accepted = RideService.accept_ride(ride.id, self.driver1)
        self.assertEqual(accepted.status, 'ACCEPTED')
        self.assertEqual(accepted.driver, self.driver1)

    # 4. Cancellation
    def test_cancellation(self):
        ride = RideService.create_ride("Kiranmayee", "A", "B", 5, 5)
        ride.status = Ride.Status.CANCELLED
        ride.save()
        self.assertEqual(ride.status, 'CANCELLED')
        self.assertFalse(ride.can_transition_to(Ride.Status.ACCEPTED))

    # 5. Invalid state changes
    def test_invalid_state_changes(self):
        ride = RideService.create_ride("Kiranmayee", "A", "B", 5, 5)
        with self.assertRaises(ValueError):
            RideService.start_ride(ride.id, self.driver1) # REQUESTED -> STARTED invalid

    # 6. Duplicate ride acceptance - MOST IMPORTANT
    def test_duplicate_ride_acceptance(self):
        ride = RideService.create_ride("Kiranmayee", "A", "B", 5, 5)
        RideService.accept_ride(ride.id, self.driver1)
        with self.assertRaises(ValueError):
            RideService.accept_ride(ride.id, self.driver2) # already ACCEPTED