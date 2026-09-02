class FareService:
    @staticmethod
    def get_fare_estimate(distance_km, duration_min):
        base = 40
        per_km = 10
        per_min = 2
        platform_fee = 10
        return base + (distance_km * per_km) + (duration_min * per_min) + platform_fee