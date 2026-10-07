"""
FareService - Business calculation moved from views - Task 3 fix
"""


class FareService:
    @staticmethod
    def calculate_fare(distance_km, base_rate=50, per_km=12):
        # Business calculation - moved from views.py BAD -> service.py GOOD
        if distance_km <= 0:
            raise ValueError("Distance must be positive")
        fare = base_rate + (distance_km * per_km)
        # Multiple conditional statements - moved from views
        if distance_km > 20:
            fare *= 0.9  # 10% discount
        elif distance_km > 10:
            fare *= 0.95
        return round(fare, 2)
