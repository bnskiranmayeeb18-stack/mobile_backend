# TASK 6 FIXES - Applied in backend

# Fix 1,2: JWT Validation in settings.py
"""
SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(minutes=15),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=1),
    'ROTATE_REFRESH_TOKENS': True,
    'BLACKLIST_AFTER_ROTATION': True,
}
"""

# Fix 3,4,5: Permission check in views.py
"""
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import PermissionDenied

@permission_classes([IsAuthenticated])
def get_ride(request, ride_id):
    ride = Ride.objects.get(id=ride_id)
    if ride.user_id!= request.user.id:
        raise PermissionDenied("Not your ride!")
    return ride
"""

# Fix 6: WebSocket auth
"""
class RideConsumer(WebsocketConsumer):
    def connect(self):
        user = self.scope["user"]
        if user.is_anonymous:
            self.close(code=4401)
            return
"""

# Fix 7: Throttling
"""
REST_FRAMEWORK = {
    'DEFAULT_THROTTLE_CLASSES': ['rest_framework.throttling.UserRateThrottle'],
    'DEFAULT_THROTTLE_RATES': {'user': '5/minute', 'anon': '100/minute'}
}
"""

# Fix 8: Serializer validation
"""
class RideSerializer(serializers.Serializer):
    fare = serializers.FloatField(min_value=0)
    pickup = serializers.CharField(required=True, allow_blank=False)
"""
