from rest_framework import serializers
from .models import Ride

class RideListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ride
        fields = ['id', 'status', 'pickup_location', 'drop_location', 'created_at', 'driver', 'rider']
        read_only_fields = fields

class RideSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ride
        fields = '__all__'