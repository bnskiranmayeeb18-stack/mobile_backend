from rest_framework import serializers
from .models import Ride

class RideSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ride
        fields = ['id', 'rider', 'pickup', 'drop', 'status', 'created_at']
        read_only_fields = ['id', 'rider', 'created_at']

class RideListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ride
        fields = ['id', 'pickup', 'drop', 'status', 'created_at']
        read_only_fields = ['id', 'created_at']

class RideCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ride
        fields = ['pickup', 'drop']  # model lo unna fields ye

class RideDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ride
        fields = ['id', 'rider', 'pickup', 'drop', 'status', 'created_at']

class RideUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ride
        fields = ['status']

class RideDeleteSerializer(serializers.Serializer):
    pass