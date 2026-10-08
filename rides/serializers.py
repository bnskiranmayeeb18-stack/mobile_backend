from rest_framework import serializers
from .models import Ride

class RideListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ride
        fields = ['id', 'rider', 'pickup', 'drop', 'status', 'created_at']
        read_only_fields = ['id', 'rider', 'created_at']

class RideCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ride
        fields = ['pickup', 'drop', 'status']