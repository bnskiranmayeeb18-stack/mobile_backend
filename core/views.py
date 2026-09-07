from django.db import connection
from django.db.models import Count, Sum, Avg, Max, Min, Q
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from.models import Ride # correct import

# ===========================
# EPIC 03 Task 3 - Implement Aggregation
# ===========================
class RideStatsView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        # Driver login ayite thana rides mathrame, lekapothe anni rides
        if hasattr(request.user, 'driver'):
            rides = Ride.objects.filter(driver=request.user.driver)
        else:
            rides = Ride.objects.all()

        stats = rides.aggregate(
            total_rides=Count('id'),
            completed_rides=Count('id', filter=Q(status='completed')),
            cancelled_rides=Count('id', filter=Q(status='cancelled')),
            total_earnings=Sum('fare', filter=Q(status='completed')),
            average_fare=Avg('fare'),
            maximum_fare=Max('fare'),
            minimum_fare=Min('fare'),
        )

        # None values ni 0 chesam
        clean_stats = {k: (0 if v is None else float(v) if isinstance(v, float) or 'fare' in k or 'earning' in k else v) for k, v in stats.items()}
        # Simple version for 0 case:
        for k in clean_stats:
            if clean_stats[k] is None:
                clean_stats[k] = 0

        return Response(clean_stats)

# ===========================
# EPIC 03 Task 4 - N+1 Queries
# ===========================

# PART A: INEFFICIENT - N+1 Problem
# PART A: INEFFICIENT
# PART A: INEFFICIENT - N+1 problem unna code
class RideListInefficientView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request):
        rides = Ride.objects.all() # No select_related
        data = []
        for ride in rides:
            # Ikkada loop lo malli DB hit avtundi - Ide N+1
            data.append({
                "id": ride.id,
                "fare": float(ride.fare) if ride.fare else 0,
                "status": ride.status,
                "customer": str(ride.customer) if hasattr(ride, 'customer') else None,
            })
        return Response({"type": "INEFFICIENT - N+1 queries", "count": len(data), "data": data})

# PART B: OPTIMIZED - Fixed with select_related
class RideListOptimizedView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request):
        rides = Ride.objects.select_related('customer').all() # FIX: driver kadu, customer
        data = []
        for ride in rides:
            data.append({
                "id": ride.id,
                "fare": float(ride.fare) if ride.fare else 0,
                "status": ride.status,
                "customer": str(ride.customer) if hasattr(ride, 'customer') else None,
            })
        return Response({"type": "OPTIMIZED with select_related('customer')", "count": len(data), "data": data})