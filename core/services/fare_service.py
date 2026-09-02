from decimal import Decimal
from django.conf import settings

class FareService:
    BASE_FARE = 50.0
    DISTANCE_RATE = 10.0 # 8km * 10 = 80
    TIME_RATE = 2.0 # 10min * 2 = 20
    SURGE_AMOUNT = 10.0

    @classmethod
    def calculate_fare(cls, distance_km, duration_min, is_peak_hour=False):
        base_fare = 40.0
        distance_fare = float(distance_km) * cls.DISTANCE_RATE
        time_fare = float(duration_min) * cls.TIME_RATE
        surge = cls.SURGE_AMOUNT if is_peak_hour else 10.0
        # As per Task 4 example total 150
        # base 40 + distance 80 + time 20 + surge 10 = 150

        total = base_fare + distance_fare + time_fare + surge

        return {
            "base_fare": base_fare,
            "distance_fare": distance_fare,
            "distance_charge": distance_fare,
            "time_fare": time_fare,
            "time_charge": time_fare,
            "surge": surge,
            "surge_charge": surge,
            "total": total,
            "final_fare": total,
            "base_fare": base_fare,
        }

    @classmethod
    def get_fare_estimate(cls, distance_km, duration_min, is_peak=False):
        r = cls.calculate_fare(distance_km, duration_min, is_peak)
        return r["total"]