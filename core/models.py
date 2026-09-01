import uuid
from django.db import models
from django.conf import settings


# Base model for UUID + Timestamps
class BaseModel(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class VehicleType(BaseModel):
    name = models.CharField(max_length=50, unique=True)  # Ex: Mini, Auto, Bike
    description = models.TextField(blank=True)

    def __str__(self):
        return self.name


class DriverProfile(BaseModel):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='driver_profile')
    license_number = models.CharField(max_length=50, unique=True)

    class Meta:
        indexes = [models.Index(fields=['license_number'])]
        constraints = [models.UniqueConstraint(fields=['license_number'], name='unique_license')]


class Vehicle(BaseModel):
    driver = models.ForeignKey(DriverProfile, on_delete=models.CASCADE, related_name='vehicles')
    vehicle_type = models.ForeignKey(VehicleType, on_delete=models.SET_NULL, null=True)
    vehicle_number = models.CharField(max_length=20, unique=True)

    class Meta:
        indexes = [models.Index(fields=['vehicle_number'])]


class RideStatus(models.TextChoices):
    REQUESTED = 'requested', 'Requested'
    ACCEPTED = 'accepted', 'Accepted'
    ONGOING = 'ongoing', 'Ongoing'
    COMPLETED = 'completed', 'Completed'
    CANCELLED = 'cancelled', 'Cancelled'


class Ride(BaseModel):
    rider = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='rides_as_rider')
    driver = models.ForeignKey(DriverProfile, on_delete=models.SET_NULL, null=True, related_name='rides_as_driver')
    vehicle = models.ForeignKey(Vehicle, on_delete=models.SET_NULL, null=True)
    status = models.CharField(max_length=20, choices=RideStatus.choices, default=RideStatus.REQUESTED)
    pickup_location = models.CharField(max_length=255)
    drop_location = models.CharField(max_length=255)
    fare = models.DecimalField(max_digits=10, decimal_places=2)

    class Meta:
        indexes = [
            models.Index(fields=['status']),
            models.Index(fields=['rider', 'status']),
        ]

class RideLocation(BaseModel):
    ride = models.ForeignKey(Ride, on_delete=models.CASCADE, related_name='location_detail')
    pickup_lat = models.FloatField()
    pickup_lng = models.FloatField()
    drop_lat = models.FloatField()
    drop_lng = models.FloatField()