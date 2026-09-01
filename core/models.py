from django.db import models
from django.contrib.auth.models import User

class VehicleType(models.Model):
    name = models.CharField(max_length=20) # Bike, Car etc

    def __str__(self):
        return self.name

class Vehicle(models.Model):
    type = models.ForeignKey(VehicleType, on_delete=models.CASCADE)
    registration_number = models.CharField(max_length=20, unique=True)

    def __str__(self):
        return self.registration_number

class DriverProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)
    name = models.CharField(max_length=100, default='Unknown')
    vehicle = models.OneToOneField(Vehicle, on_delete=models.CASCADE, null=True, blank=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name

    def __str__(self):
        return self.name


Driver = DriverProfile
Ride = None
RideLocation = None