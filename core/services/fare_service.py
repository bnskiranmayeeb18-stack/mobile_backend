class FareService:
    @staticmethod
    def calculate_fare(distance_km, duration_min, is_peak_hour=False):
        # Formula from doc: fare = (distance_km * 15) + (duration * 2)
        base_fare = (distance_km * 15) + (duration_min * 2)
        if is_peak_hour:
            base_fare = base_fare * 1.5  # surge pricing
        return round(base_fare, 2)