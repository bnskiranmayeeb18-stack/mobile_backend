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
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='requested')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.rider} - {self.pickup}->{self.drop}"

class Booking(Ride):
    class Meta:
        proxy = True
