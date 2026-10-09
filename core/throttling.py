from rest_framework.throttling import UserRateThrottle, AnonRateThrottle

class LoginRateThrottle(AnonRateThrottle):
    scope = 'login'
    rate = '5/minute'

class SensitiveOpsThrottle(UserRateThrottle):
    scope = 'sensitive'
    rate = '10/minute'

class BurstThrottle(UserRateThrottle):
    scope = 'burst'
    rate = '20/minute'