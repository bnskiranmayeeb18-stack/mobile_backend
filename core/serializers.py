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
        read_only_fields = ['status', 'driver']