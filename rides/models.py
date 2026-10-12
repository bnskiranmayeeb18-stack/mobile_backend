def service_image_path(instance, filename):
    return f"services/{filename}"

from django.db import models
from django.contrib.auth.models import User

class Ride(models.Model):
    STATUS_CHOICES = [
        ('requested','requested'),
        ('accepted','accepted'),
        ('started','started'),
        ('completed','completed'),
        ('cancelled','cancelled'),
    ]
    rider = models.ForeignKey(User, on_delete=models.CASCADE, related_name='rides')
    driver = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='driven_rides')
    pickup = models.CharField(max_length=255)
    drop = models.CharField(max_length=255)
    pickup_lat = models.FloatField(null=True, blank=True)
    pickup_lng = models.FloatField(null=True, blank=True)
    dest_lat = models.FloatField(null=True, blank=True)
    dest_lng = models.FloatField(null=True, blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='requested')
    ride_type = models.CharField(max_length=20, default='STANDARD')
    created_at = models.DateTimeField(auto_now_add=True)

class DriverProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    is_online = models.BooleanField(default=False)
