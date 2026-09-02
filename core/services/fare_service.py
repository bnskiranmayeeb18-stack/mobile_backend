from decimal import Decimal
from django.conf import settings

class FareService:
    # Configurable values - not hardcoded! Can be moved to settings.py
    BASE_FARE = getattr(settings, 'FARE_BASE', Decimal('50.00'))
    DISTANCE_RATE_PER_KM = getattr(settings, 'FARE_PER_KM', Decimal('15.00'))
    TIME_RATE_PER_MIN = getattr(settings, 'FARE_PER_MIN', Decimal('2.00'))
    SURGE_MULTIPLIER = getattr(settings, 'FARE_SURGE', Decimal('1.5'))
    MIN_FARE = getattr(settings, 'FARE_MIN', Decimal('80.00'))

    @classmethod
    def calculate_fare(cls, distance_km, duration_min, is_peak_hour=False, is_surge=False):
        """
        Formula:
        Base Fare
        + Distance Charge (distance_km * rate)
        + Time Charge (duration_min * rate)
        + Surge Charge (if applicable)
        = Final Fare
        """
        distance_km = Decimal(str(distance_km))
        duration_min = Decimal(str(duration_min))

        base_fare = cls.BASE_FARE
        distance_charge = distance_km * cls.DISTANCE_RATE_PER_KM
        time_charge = duration_min * cls.TIME_RATE_PER_MIN

        subtotal = base_fare + distance_charge + time_charge

        surge_charge = Decimal('0.00')
        if is_peak_hour or is_surge:
            surge_charge = subtotal * (cls.SURGE_MULTIPLIER - 1)
            final_fare = subtotal * cls.SURGE_MULTIPLIER
        else:
            final_fare = subtotal

        # Ensure minimum fare
        if final_fare < cls.MIN_FARE:
            final_fare = cls.MIN_FARE

        return {
            "base_fare": float(base_fare),
            "distance_charge": float(distance_charge),
            "time_charge": float(time_charge),
            "surge_charge": float(surge_charge),
            "final_fare": float(round(final_fare, 2)),
            "breakup": f"{base_fare} + {distance_charge} + {time_charge} + {surge_charge} = {final_fare}"
        }

    @classmethod
    def get_fare_estimate(cls, distance_km, duration_min):
        """Simple wrapper for quick estimate"""
        result = cls.calculate_fare(distance_km, duration_min)
        return result['final_fare']

    # Fare Config - Task 3 Configurable Values
    FARE_BASE = 50.00
    FARE_PER_KM = 15.00
    FARE_PER_MIN = 2.00
    FARE_SURGE = 1.5
    FARE_MIN = 80.00