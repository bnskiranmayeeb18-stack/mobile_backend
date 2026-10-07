"""
constants.py - All magic numbers, strings, status - Repeated code centralized
"""


# Ride Status
class RideStatus:
    PENDING = "pending"
    ACCEPTED = "accepted"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    CANCELLED = "cancelled"
    REQUIRES_APPROVAL = "requires_approval"

    CHOICES = [
        (PENDING, "Pending"),
        (ACCEPTED, "Accepted"),
        (IN_PROGRESS, "In Progress"),
        (COMPLETED, "Completed"),
        (CANCELLED, "Cancelled"),
    ]

    ALLOWED_TRANSITIONS = {
        PENDING: [ACCEPTED, CANCELLED],
        ACCEPTED: [IN_PROGRESS, CANCELLED],
        IN_PROGRESS: [COMPLETED],
        COMPLETED: [],
        CANCELLED: [],
    }


# Cache TTL
CACHE_TTL = {
    "DRIVER": 3600,  # 1 hour
    "RIDE": 1800,  # 30 min
    "RIDE_LIST": 1800,
    "NEARBY_DRIVERS": 60,  # 60 sec
    "USER_PROFILE": 3600,
    "NOTIFICATIONS": 1800,
}

# Cache Keys
CACHE_KEYS = {
    "DRIVER": "driver_{id}",
    "RIDE": "ride_{id}",
    "USER_RIDES": "rides_{user_id}",
    "NEARBY": "available_drivers_{lat}_{lng}",
    "USER": "user_{id}",
}

# Fare Constants - Repeated in views before
FARE = {
    "BASE_RATE": 50,
    "PER_KM": 12,
    "DISCOUNT_10_KM": 0.95,  # 5% discount
    "DISCOUNT_20_KM": 0.90,  # 10% discount
    "MIN_DISTANCE": 0.5,
    "MAX_DISTANCE": 100,
}

# API Messages - Repeated code - Task 6 ki kuda use
MESSAGES = {
    "RIDE_CREATED": "Ride created successfully",
    "RIDE_UPDATED": "Ride status updated successfully",
    "RIDE_LIST": "Rides fetched successfully",
    "DRIVER_FOUND": "Nearby drivers found",
    "VALIDATION_ERROR": "Validation failed",
    "NOT_FOUND": "Resource not found",
    "PERMISSION_DENIED": "You do not have permission",
}
