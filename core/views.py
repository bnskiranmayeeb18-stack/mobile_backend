from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.db.models import Count, Avg
from .models import Ride
from .serializers import RideSerializer
from .pagination import RidePagination

@api_view(['GET'])
def ride_list(request):
    rides = Ride.objects.all().order_by('-id')
    paginator = RidePagination()
    result = paginator.paginate_queryset(rides, request)
    serializer = RideSerializer(result, many=True)
    return paginator.get_paginated_response(serializer.data)

@api_view(['GET'])
def optimized_rides(request):
    # user kadu, customer - correct chesa
    rides = Ride.objects.select_related('customer').all().order_by('-created_at')
    paginator = RidePagination()
    result = paginator.paginate_queryset(rides, request)
    serializer = RideSerializer(result, many=True)
    return paginator.get_paginated_response(serializer.data)

@api_view(['GET'])
def ride_stats(request):
    # distance kadu, fare - correct chesa
    stats = Ride.objects.aggregate(
        total_rides=Count('id'),
        avg_fare=Avg('fare')
    )
    return Response(stats)

@api_view(['GET'])
def ride_history(request):
    user_id = request.query_params.get('user_id')
    if user_id:
        rides = Ride.objects.filter(customer_id=user_id).order_by('-created_at')
    else:
        rides = Ride.objects.all().order_by('-created_at')
    serializer = RideSerializer(rides, many=True)
    return Response(serializer.data)