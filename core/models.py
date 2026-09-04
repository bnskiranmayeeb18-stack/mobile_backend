from django.db import models
from django.contrib.auth.models import User

class Ride(models.Model):
    STATUS_CHOICES = [
        ('REQUESTED','REQUESTED'),
        ('ACCEPTED','ACCEPTED'),
        ('STARTED','STARTED'),
        ('COMPLETED','COMPLETED'),
        ('CANCELLED','CANCELLED'),
    ]
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True, related_name='rides')
    customer = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True, related_name='rides_as_customer')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='REQUESTED')
    fare = models.FloatField(null=True, blank=True)
    distance_km = models.FloatField(null=True, blank=True)
    duration_min = models.FloatField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True)

    def __str__(self):
        return f"Ride {self.id} - {self.status}"