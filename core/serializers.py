from rest_framework import serializers
from.models import VehicleType, Vehicle, DriverProfile

class VehicleTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = VehicleType
        fields = ['id', 'name']

class VehicleSerializer(serializers.ModelSerializer):
    type = VehicleTypeSerializer(read_only=True)
    type_id = serializers.PrimaryKeyRelatedField(queryset=VehicleType.objects.all(), write_only=True, source='type')

    class Meta:
        model = Vehicle
        fields = ['id', 'type', 'type_id', 'registration_number']

class DriverProfileSerializer(serializers.ModelSerializer):
    vehicle = VehicleSerializer(read_only=True)

    class Meta:
        model = DriverProfile
        fields = ['id', 'name', 'vehicle']