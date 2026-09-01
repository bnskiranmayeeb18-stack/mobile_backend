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

class DriverProfile(models.Model): # old name
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    vehicle = models.OneToOneField(Vehicle, on_delete=models.CASCADE)

    def __str__(self):
        return self.name


Driver = DriverProfile
Ride = None
RideLocation = None