from rest_framework.throttling import AnonRateThrottle, UserRateThrottle

class BurstRateThrottle(UserRateThrottle):
    scope = 'burst'

class SustainedRateThrottle(UserRateThrottle):
    scope = 'sustained'
    rate = '100/hour'

class BurstThrottle(UserRateThrottle):
    scope = 'burst'

class AnonBurstThrottle(AnonRateThrottle):
    scope = 'anon'