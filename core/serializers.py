from rest_framework import serializers
from .models import Profile
from django.contrib.auth.models import User
import re

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email']

    def validate_email(self, value):
        if not value:
            raise serializers.ValidationError("Email is required")
        # Update time lo same user email ayite allow cheyali
        if self.instance and self.instance.email == value:
            return value
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError("Email already exists")
        return value

class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ['id', 'full_name', 'phone_number', 'image']
        # read_only_fields = ['id']

    def validate_full_name(self, value):
        # Empty ayite ok, but isthe 3 chars kante ekkuva undali
        if value:
            if len(value.strip()) < 3:
                raise serializers.ValidationError("Full name must be at least 3 characters")
            if len(value.strip()) > 50:
                raise serializers.ValidationError("Full name must be less than 50 characters")
        return value

    def validate_phone_number(self, value):
        if value:
            # Indian mobile validation: 10 digits, 6-9 start
            if not re.match(r'^[6-9]\d{9}$', value):
                raise serializers.ValidationError("Enter valid 10-digit Indian mobile number")
        return value

    def validate_image(self, value):
        if value:
            # Size < 2MB
            if value.size > 2 * 1024 * 1024:
                raise serializers.ValidationError("Image size should be less than 2MB")
            # Extension check
            valid_extensions = ['jpg', 'jpeg', 'png']
            ext = value.name.split('.')[-1].lower()
            if ext not in valid_extensions:
                raise serializers.ValidationError("Only jpg, jpeg, png allowed")
        return value