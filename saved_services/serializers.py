from rest_framework import serializers
from .models import SavedService

class SavedServiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = SavedService
        fields = "__all__"