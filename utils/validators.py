"""
validators.py - Common validation moved from views/serializers
"""
from rest_framework import serializers
from.constants import FARE

def validate_lat_lng(lat, lng):
    # Repeated code - lat/lng validation in many views
    if not (-90 <= lat <= 90):
        raise serializers.ValidationError("Invalid latitude -90 to 90")
    if not (-180 <= lng <= 180):
        raise serializers.ValidationError("Invalid longitude -180 to 180")
    return True

def validate_distance(distance):
    if distance <= 0:
        raise serializers.ValidationError("Distance must be positive")
    if distance < FARE['MIN_DISTANCE']:
        raise serializers.ValidationError(f"Min distance {FARE['MIN_DISTANCE']} km")
    if distance > FARE['MAX_DISTANCE']:
        raise serializers.ValidationError(f"Max distance {FARE['MAX_DISTANCE']} km")
    return True

def validate_pickup_drop(pickup, drop):
    if not pickup or len(pickup.strip()) < 3:
        raise serializers.ValidationError("Pickup location required min 3 chars")
    if not drop or len(drop.strip()) < 3:
        raise serializers.ValidationError("Drop location required min 3 chars")
    if pickup.lower() == drop.lower():
        raise serializers.ValidationError("Pickup and drop cannot be same")
    return True

def validate_status_transition(current_status, new_status):
    from.constants import RideStatus
    allowed = RideStatus.ALLOWED_TRANSITIONS.get(current_status, [])
    if new_status not in allowed:
        raise serializers.ValidationError(f"Cannot transition {current_status} -> {new_status}. Allowed: {allowed}")
    return True