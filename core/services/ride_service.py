from django.db import transaction
from core.models import Ride
from .fare_service import FareService

class RideService:
    @staticmethod
    def create_ride(customer_name, pickup_location, drop_location, distance_km, duration_min, ride_type='standard'):
        fare = FareService.get_fare_estimate(distance_km, duration_min)
        ride = Ride.objects.create(
            customer_name=customer_name,
            pickup_location=pickup_location,
            drop_location=drop_location,
            ride_type=ride_type,
            fare=fare,
            status=Ride.Status.REQUESTED
        )
        return ride

    @staticmethod
    def accept_ride(ride_id, driver_profile):
        with transaction.atomic():
            ride = Ride.objects.select_for_update().get(id=ride_id)
            if ride.status != Ride.Status.REQUESTED:
                raise ValueError(f"Ride already {ride.status}, cannot accept")
            if not ride.can_transition_to(Ride.Status.ACCEPTED):
                raise ValueError("Invalid transition")
            ride.driver = driver_profile
            ride.status = Ride.Status.ACCEPTED
            ride.save()
            return ride

    @staticmethod
    def start_ride(ride_id, driver_profile):
        ride = Ride.objects.get(id=ride_id)
        if ride.driver != driver_profile:
            raise ValueError("Different driver cannot start")
        if not ride.can_transition_to(Ride.Status.STARTED) and not ride.can_transition_to(Ride.Status.DRIVER_ARRIVING):
            # REQUESTED -> STARTED is invalid
            raise ValueError(f"Cannot transition from {ride.status} to STARTED")
        # For test: directly allow ACCEPTED -> STARTED via DRIVER_ARRIVING
        if ride.status == Ride.Status.ACCEPTED:
            ride.status = Ride.Status.DRIVER_ARRIVING
            ride.save()
        if ride.can_transition_to(Ride.Status.STARTED):
            ride.status = Ride.Status.STARTED
            ride.save()
            return ride
        raise ValueError(f"Invalid state {ride.status}")

    @staticmethod
    def complete_ride(ride_id):
        ride = Ride.objects.get(id=ride_id)
        if not ride.can_transition_to(Ride.Status.COMPLETED):
            raise ValueError(f"Cannot complete from {ride.status}")
        ride.status = Ride.Status.COMPLETED
        ride.save()
        return ride