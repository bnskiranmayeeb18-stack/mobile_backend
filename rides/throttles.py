from rest_framework.throttling import SimpleRateThrottle

class LoginRateThrottle(SimpleRateThrottle):
    scope = 'login'
    def get_cache_key(self, request, view):
        return self.get_ident(request)

class RegisterRateThrottle(SimpleRateThrottle):
    scope = 'register'
    def get_cache_key(self, request, view):
        return self.get_ident(request)

class OTPRateThrottle(SimpleRateThrottle):
    scope = 'otp'

class RideCreateRateThrottle(SimpleRateThrottle):
    scope = 'ride_create'
    def get_cache_key(self, request, view):
        if request.user.is_authenticated:
            return f"user_{request.user.pk}"
        return self.get_ident(request)