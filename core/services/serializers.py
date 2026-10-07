from rest_framework import serializers

from core.models import Ride


class RideSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ride
        fields = [
            "id",
            "pickup_location",
            "drop_location",
            "distance",
            "fare",
            "status",
            "created_at",
        ]
        read_only_fields = ["fare", "status"]

    def validate_distance(self, value):
        # Validation ONLY in serializer - moved from views
        if value <= 0:
            raise serializers.ValidationError("Distance must be positive")
        if value > 100:
            raise serializers.ValidationError("Distance too large")
        return value

    def validate_pickup_location(self, value):
        if not value or len(value) < 3:
            raise serializers.ValidationError("Pickup required")
        return value


class RideStatusUpdateSerializer(serializers.Serializer):
    status = serializers.ChoiceField(
        choices=["accepted", "in_progress", "completed", "cancelled"]
    )
