class FareService:
    BASE_FARE = 40
    PER_KM_RATE = 10
    PER_MIN_RATE = 2
    PLATFORM_FEE = 10

    @classmethod
    def get_fare_estimate(cls, distance_km: float, duration_min: float) -> float:
        # Single responsibility - only fare logic
        distance_fare = distance_km * cls.PER_KM_RATE
        time_fare = duration_min * cls.PER_MIN_RATE
        return cls.BASE_FARE + distance_fare + time_fare + cls.PLATFORM_FEE

    # Alias for old code compatibility
    @classmethod
    def calculate_fare(cls, distance_km, duration_min, is_peak_hour=False):
        total = cls.get_fare_estimate(distance_km, duration_min)
        if is_peak_hour:
            total += 10 # surge
        return {"total": total}