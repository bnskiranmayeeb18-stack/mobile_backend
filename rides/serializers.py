from rest_framework import serializers
from.models import Ride

class RideSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ride
        fields = ['id', 'rider', 'driver', 'user', 'pickup', 'drop', 'status', 'idempotency_key', 'version', 'created_at', 'updated_at']
        read_only_fields = ['id', 'version', 'created_at', 'updated_at', 'rider', 'driver', 'user']

    def validate_status(self, value):
        valid = ['requested', 'accepted', 'started', 'completed', 'cancelled',
                 'pending', 'in_progress', 'COMPLETED', 'REQUESTED']
        # normalize lowercase for validation but keep original
        if value.lower() not in [v.lower() for v in valid]:
            raise serializers.ValidationError("Invalid status")
        return value.lower()
