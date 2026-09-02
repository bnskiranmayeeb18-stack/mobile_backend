from core.models import Ride

class EligibilityService:
    @staticmethod
    def can_request_ride(user):
        has_active = Ride.objects.filter(
            user=user,
            status__in=['requested', 'accepted', 'started']
        ).exists()
        if has_active:
            return False, "User already has an active ride"
        return True, "Eligible"

    @staticmethod
    def can_accept_ride(driver):
        has_active = Ride.objects.filter(
            driver=driver,
            status__in=['accepted', 'started']
        ).exists()
        if has_active:
            return False, "Driver already has an active ride"
        return True, "Eligible"