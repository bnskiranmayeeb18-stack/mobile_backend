from django.db.models import Count

from core.models import Ride


def get_optimized_rides():
    return Ride.objects.select_related("user", "driver", "vehicle").all()


def get_user_ride_stats(user):
    return (
        Ride.objects.filter(user=user)
        .values("status")
        .annotate(count=Count("id"))
    )


def get_driver_performance():
    return (
        Ride.objects.values("driver")
        .annotate(total_rides=Count("id"))
        .order_by("-total_rides")
    )


def get_rides_with_prefetch():
    return Ride.objects.prefetch_related("user", "driver").all()
