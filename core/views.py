from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.db.models import Count, Avg
from .models import Ride
from .serializers import RideSerializer
from .pagination import RidePagination


@api_view(['GET'])
def ride_list(request):
    # Refactored: select_related added to avoid N+1 when serializer accesses customer
    rides = Ride.objects.select_related('customer').all().order_by('-id')
    paginator = RidePagination()
    result = paginator.paginate_queryset(rides, request)
    serializer = RideSerializer(result, many=True)
    return paginator.get_paginated_response(serializer.data)


@api_view(['GET'])
def optimized_rides(request):
    # Refactored: No queries inside loops, single DB call with select_related
    rides = Ride.objects.select_related('customer').all().order_by('-created_at')
    paginator = RidePagination()
    result = paginator.paginate_queryset(rides, request)
    serializer = RideSerializer(result, many=True)
    return paginator.get_paginated_response(serializer.data)


@api_view(['GET'])
def ride_stats(request):
    # Refactored: Single aggregate query instead of multiple calls
    stats = Ride.objects.aggregate(
        total_rides=Count('id'),
        avg_fare=Avg('fare')
    )
    return Response(stats)


@api_view(['GET'])
def ride_history(request):
    # Refactored: Removed duplicate query logic, added select_related
    rides = Ride.objects.select_related('customer').all().order_by('-created_at')
    user_id = request.query_params.get('user_id')
    if user_id:
        rides = rides.filter(customer_id=user_id)

    paginator = RidePagination()
    result = paginator.paginate_queryset(rides, request)
    serializer = RideSerializer(result, many=True)
    return paginator.get_paginated_response(serializer.data)