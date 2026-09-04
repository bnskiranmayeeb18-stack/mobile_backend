from rest_framework import serializers
from.models import Vehicle, DriverProfile, Ride

class VehicleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vehicle
        fields = ['id', 'vehicle_number', 'vehicle_type', 'model', 'is_available']
        read_only_fields = ['id']

class DriverProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = DriverProfile
        fields = ['id', 'user', 'license_number', 'is_verified', 'rating']
        read_only_fields = ['id', 'is_verified', 'rating']

class RideSerializer(serializers.ModelSerializer):
    # Naming: Clear field names
    customer_name = serializers.CharField(source='passenger.username', read_only=True)

    class Meta:
        model = Ride
        fields = [
            'id', 'passenger', 'customer_name', 'pickup_location',
            'drop_location', 'ride_type', 'status', 'driver',
            'created_at', 'fare'
        ]
        read_only_fields = ['id', 'passenger', 'status', 'created_at', 'driver', 'fare']

    def validate_pickup_location(self, value):
        if not value or not value.strip():
            raise serializers.ValidationError("Pickup location is required.")
        if len(value.strip()) < 3:
            raise serializers.ValidationError("Pickup location too short.")
        return value.strip()

    def validate_drop_location(self, value):
        if not value or not value.strip():
            raise serializers.ValidationError("Drop location is required.")
        return value.strip()

    def validate(self, data):
        pickup = data.get('pickup_location', '').strip()
        drop = data.get('drop_location', '').strip()
        ride_type = data.get('ride_type')

        # 1. Pickup!= Drop (Functions: small validations)
        if pickup.lower() == drop.lower():
            raise serializers.ValidationError(
                {"drop_location": "Pickup and drop cannot be same."}
            )

        # 2. Ride type valid (Queries: efficient)
        valid_types = [choice[0] for choice in Ride.RIDE_TYPE_CHOICES]
        if ride_type not in valid_types:
            raise serializers.ValidationError(
                {"ride_type": f"Invalid ride type. Valid: {valid_types}"}
            )

        # 3. No conflicting active ride (Services logic + Queries)
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            has_active = Ride.objects.filter(
                passenger=request.user,
                status__in=['REQUESTED', 'ACCEPTED', 'ONGOING']
            ).exists()
            if has_active:
                raise serializers.ValidationError(
                    "You already have an active ride. Complete it first."
                )

        return data