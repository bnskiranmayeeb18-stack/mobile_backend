import re
from rest_framework import serializers
from .models import DriverProfile, Vehicle, VehicleType, Ride, RideLocation

class VehicleTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = VehicleType
        fields = '__all__'

class DriverProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = DriverProfile
        fields = '__all__'

class VehicleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vehicle
        fields = '__all__'

    def validate_vehicle_number(self, value):
        pattern = r'^[A-Z]{2}[0-9]{1,2}[A-Z]{1,2}[0-9]{4}$'
        clean_value = value.replace(" ", "").upper()
        if not re.match(pattern, clean_value):
            raise serializers.ValidationError("Invalid vehicle registration number. Eg: AP05AB1234")
        return clean_value

    def validate(self, data):
        if self.instance is None: # Create time lo mathrame duplicate check
            if Vehicle.objects.filter(
                driver=data.get('driver'),
                vehicle_number=data.get('vehicle_number')
            ).exists():
                raise serializers.ValidationError("Duplicate vehicle for this driver")
        return data

class RideSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ride
        fields = '__all__'

class RideLocationSerializer(serializers.ModelSerializer):
    class Meta:
        model = RideLocation
        fields = '__all__'