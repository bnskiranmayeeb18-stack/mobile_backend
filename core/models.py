from django.db import models
from django.contrib.auth.models import User

class Vehicle(models.Model):
    registration_number = models.CharField(max_length=30, unique=True)
    def __str__(self): return self.registration_number

class DriverProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)
    name = models.CharField(max_length=100, default="Unknown")
    vehicle = models.OneToOneField(Vehicle, on_delete=models.CASCADE, null=True, blank=True)
    is_active = models.BooleanField(default=True)
    def __str__(self): return self.name

class Ride(models.Model):
    STATUS = [('pending','pending'),('accepted','accepted'),('cancelled','cancelled'),('completed','completed')]
    customer_name = models.CharField(max_length=100)
    status = models.CharField(max_length=20, choices=STATUS, default='pending')
    driver = models.ForeignKey(DriverProfile, null=True, blank=True, on_delete=models.SET_NULL, related_name='rides')
    def __str__(self): return f"{self.customer_name} - {self.status}"