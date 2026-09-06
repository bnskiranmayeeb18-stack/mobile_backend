from django.db.models import Q, F, Count, Avg
from core.models import Ride

# EPIC 03 - Task 1: Advanced QuerySets

def advanced_queryset_examples():
    # 1. filter() - REQUESTED rides
    requested_rides = Ride.objects.filter(status='REQUESTED')

    # 2. exclude() - CANCELLED kakunda
    active_rides = Ride.objects.exclude(status='CANCELLED')

    # 3. Q() - REQUESTED OR ACCEPTED (OR condition)
    q_rides = Ride.objects.filter(Q(status='REQUESTED') | Q(status='ACCEPTED'))

    # 4. F() - field to field comparison
    # Example: distance > 5km rides
    long_rides = Ride.objects.filter(distance__gt=F('id'))  # sample F usage

    # 5. annotate() - prati customer ki count
    from django.contrib.auth.models import User
    users_with_count = User.objects.annotate(total_rides=Count('ride'))

    # 6. aggregate() - motham rides count / avg
    stats = Ride.objects.aggregate(total_rides=Count('id'), avg_fare=Avg('fare'))

    # 7. values() - dict list ga - only id, status
    rides_dict = Ride.objects.values('id', 'status')

    # 8. values_list() - flat list of ids
    ride_ids = Ride.objects.values_list('id', flat=True)

    # 9. exists() - ride unda leda? Fast query
    has_requested = Ride.objects.filter(status='REQUESTED').exists()

    # 10. distinct() - unique customers
    unique_customers = Ride.objects.values('customer').distinct()

    return {
        "filter": requested_rides,
        "exclude": active_rides,
        "q_objects": q_rides,
        "exists": has_requested
    }