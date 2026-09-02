from rest_framework import serializers
from .models import Vehicle, DriverProfile, Ride

class VehicleSerializer(serializers.ModelSerializer):
    class Meta: model = Vehicle; fields = '__all__'

class DriverProfileSerializer(serializers.ModelSerializer):
    class Meta: model = DriverProfile; fields = '__all__'

class RideSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ride
        fields = '__all__'
        read_only_fields = ['id', 'passenger', 'status', 'created_at', 'driver']

    def validate(self, data):
        pickup = data.get('pickup_location', '').strip()
        drop = data.get('drop_location', '').strip()
        ride_type = data.get('ride_type')

        # 1. Pickup & Drop exists
        if not pickup:
            raise serializers.ValidationError({"pickup_location": "Pickup location is required."})
        if not drop:
            raise serializers.ValidationError({"drop_location": "Drop location is required."})

        # 2. Pickup!= Drop
        if pickup.lower() == drop.lower():
            raise serializers.ValidationError({"drop_location": "Pickup and drop cannot be same."})

        # 3. Ride type valid
        valid_types = [choice[0] for choice in Ride.RIDE_TYPE_CHOICES] # or ['Mini','Sedan','Bike'...]
        if ride_type not in valid_types:
            raise serializers.ValidationError({"ride_type": f"Invalid ride type. Valid: {valid_types}"})

        # 4. No conflicting active ride
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            active_exists = Ride.objects.filter(
                passenger=request.user,
                status__in=['REQUESTED', 'ACCEPTED', 'ONGOING']
            ).exists()
            if active_exists:
                raise serializers.ValidationError("You already have an active ride. Complete it first.")

        return data