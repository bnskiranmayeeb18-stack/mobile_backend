from rest_framework import serializers
from .models import Ride

class RideSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ride
        fields = '__all__'
    
    def validate_pickup(self, value):
        if not value or not value.strip():
            raise serializers.ValidationError("pickup required")
        return value

    def validate_drop(self, value):
        if not value or not value.strip():
            raise serializers.ValidationError("drop required")
        return value
