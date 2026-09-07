from django.db.models import Q, F, Count, Sum, Avg
from .models import Ride
from django.contrib.auth import get_user_model
User = get_user_model()

# 1. filter()
q1 = Ride.objects.filter(pickup_location="Nellore")

# 2. exclude()
q2 = Ride.objects.exclude(status="CANCELLED")

# 3. Q() - OR query
q3 = Ride.objects.filter(Q(pickup_location="Nellore") | Q(drop_location="Tirupati"))

# 4. F() - field comparison
q4 = Ride.objects.filter(fare__gt=F('id'))

# 5. annotate()
q5 = User.objects.annotate(total_rides=Count('ride'))

# 6. aggregate()
q6 = Ride.objects.aggregate(total=Sum('fare'), avg=Avg('fare'))

# 7. values()
q7 = Ride.objects.values('pickup_location', 'drop_location')

# 8. values_list()
q8 = Ride.objects.values_list('fare', flat=True)

# 9. exists()
q9 = Ride.objects.filter(status="REQUESTED").exists()

# 10. distinct()
q10 = Ride.objects.values_list('pickup_location', flat=True).distinct()

print("All 10 Advanced Queries Ready!")