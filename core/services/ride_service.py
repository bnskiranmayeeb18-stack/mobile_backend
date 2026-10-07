# services/ride_service.py - Task 4 + Task 5 combined
from django.core.cache import cache

from utils.constants import CACHE_KEYS, CACHE_TTL, RideStatus
from utils.exceptions import PermissionDeniedError, ResourceNotFoundError
from utils.helpers import get_cache_or_db, invalidate_cache_patterns
from utils.validators import (validate_distance, validate_pickup_drop,
                              validate_status_transition)


from .fare_service import FareService
from .notification_service import NotificationService


class RideService:
    @staticmethod
    def create_ride(user, validated_data):
        pickup = validated_data.get("pickup_location")
        drop = validated_data.get("drop_location")
        distance = validated_data.get("distance", 5)

        validate_pickup_drop(pickup, drop)
        validate_distance(distance)

        fare = FareService.calculate_fare(distance)
        status = RideStatus.PENDING
        if distance > 50:
            status = RideStatus.REQUIRES_APPROVAL

        from rides.models import Ride

        ride = Ride.objects.create(
            user=user,
            pickup_location=pickup,
            drop_location=drop,
            distance=distance,
            fare=fare,
            status=status,
        )
        NotificationService.send_ride_created(user, ride)
        cache.set(
            CACHE_KEYS["RIDE"].format(id=ride.id),
            ride,
            timeout=CACHE_TTL["RIDE"],
        )
        return ride

    @staticmethod
    def get_user_rides(user):
        def db_call():
            from rides.models import Ride

            return list(
                Ride.objects.filter(user=user)
                .select_related("user", "driver")
                .order_by("-created_at")
            )

        rides, _ = get_cache_or_db(
            CACHE_KEYS["USER_RIDES"].format(user_id=user.id),
            db_call,
            CACHE_TTL["RIDE_LIST"],
        )
        return rides

    @staticmethod
    def get_ride_by_id(ride_id, user):
        def db_call():
            from rides.models import Ride

            try:
                return Ride.objects.select_related("user", "driver").get(
                    id=ride_id
                )
            except Ride.DoesNotExist:
                raise ResourceNotFoundError(f"Ride {ride_id} not found")

        ride, _ = get_cache_or_db(
            CACHE_KEYS["RIDE"].format(id=ride_id), db_call, CACHE_TTL["RIDE"]
        )
        if ride.user != user:
            raise PermissionDeniedError("Not owner")
        return ride

    @staticmethod
    def update_ride_status(ride_id, new_status, user):
        ride = RideService.get_ride_by_id(ride_id, user)
        validate_status_transition(ride.status, new_status)
        ride.status = new_status
        ride.save()
        invalidate_cache_patterns(
            [
                CACHE_KEYS["RIDE"].format(id=ride_id),
                CACHE_KEYS["USER_RIDES"].format(user_id=ride.user.id),
            ]
        )
        NotificationService.send_status_update(ride.user, ride, new_status)
        return ride
