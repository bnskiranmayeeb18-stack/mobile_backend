from rest_framework import serializers
from rides.models import Booking

class BookingSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    service_type = serializers.CharField(max_length=500, required=False)
    service_name = serializers.CharField(max_length=500, required=False)
    price = serializers.FloatField(required=False)
    status = serializers.CharField(read_only=True)
    customer = serializers.IntegerField(read_only=True)

    def validate_service_type(self, value):
        if value and len(value) > 500:
            raise serializers.ValidationError("Too long max 500")
        return value

    def validate_price(self, value):
        if value is not None and value < 0:
            raise serializers.ValidationError("Negative not allowed")
        return value

    def validate(self, data):
        if not data.get('service_type') and not data.get('service_name'):
            # For empty test we want 400, not 500
            raise serializers.ValidationError({"service_type": "This field is required"})
        if data.get('service_type') and not data.get('service_name'):
            data['service_name'] = data['service_type']
        return data

    def to_representation(self, instance):
        return {
            'id': getattr(instance, 'id', None),
            'service_name': getattr(instance, 'service_name', ''),
            'service_type': getattr(instance, 'service_name', ''),
            'status': getattr(instance, 'status', ''),
            'customer': getattr(instance, 'customer_id', None),
        }
