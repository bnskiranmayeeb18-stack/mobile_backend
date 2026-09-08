from rest_framework import serializers
from .models import Ride, DriverLocation

class RideSerializer(serializers.ModelSerializer):
    customer_username = serializers.CharField(source='customer.username', read_only=True)
    class Meta:
        model = Ride
        fields = ['id', 'customer', 'customer_username', 'pickup_location', 'drop_location', 'fare', 'created_at']

class DriverLocationSerializer(serializers.ModelSerializer):
    class Meta:
        model = DriverLocation
        fields = ['id', 'driver', 'latitude', 'longitude', 'accuracy', 'updated_at']