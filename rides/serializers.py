from rest_framework import serializers
from .models import Ride, DriverProfile


class RideCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ride
        fields = ['id', 'pickup_lat', 'pickup_lng', 'dest_lat', 'dest_lng', 'ride_type']

    def validate(self, data):
        if abs(data['pickup_lat']) > 90 or abs(data['dest_lat']) > 90:
            raise serializers.ValidationError("Invalid latitude")
        # Check active ride
        user = self.context['request'].user
        if Ride.objects.filter(passenger=user, status__in=['REQUESTED', 'MATCHED', 'ACCEPTED', 'STARTED']).exists():
            raise serializers.ValidationError({"active_ride": "You already have an active ride"})
        return data


class RideSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ride
        fields = '__all__'
        read_only_fields = ['passenger', 'driver', 'status', 'version']


class DriverLocationSerializer(serializers.ModelSerializer):
    class Meta:
        model = DriverProfile
        fields = ['is_online', 'current_lat', 'current_lng']