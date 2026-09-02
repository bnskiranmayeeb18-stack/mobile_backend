from django.db import transaction
from core.models import Ride
from.fare_service import FareService
from.eligibility_service import EligibilityService

class RideService:
    @staticmethod
    @transaction.atomic
    def create_ride(user, pickup, drop, distance_km, duration_min):
        eligible, msg = EligibilityService.can_request_ride(user)
        if not eligible:
            raise ValueError(msg)

        fare = FareService.get_fare_estimate(distance_km, duration_min)

        ride = Ride.objects.create(
            user=user,
            pickup_location=pickup,
            drop_location=drop,
            distance_km=distance_km,
            duration_min=duration_min,
            fare=fare,
            status='requested'
        )
        return ride

    @staticmethod
    @transaction.atomic
    def accept_ride(ride_id, driver):
        eligible, msg = EligibilityService.can_accept_ride(driver)
        if not eligible:
            raise ValueError(msg)
        ride = Ride.objects.select_for_update().get(id=ride_id)
        ride.driver = driver
        ride.status = 'accepted'
        ride.save()
        return ride

    @staticmethod
    @transaction.atomic
    def complete_ride(ride_id):
        ride = Ride.objects.select_for_update().get(id=ride_id)
        ride.status = 'completed'
        ride.save()
        return ride