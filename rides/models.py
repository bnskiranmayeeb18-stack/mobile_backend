from django.db import models
from django.contrib.auth.models import User

class Ride(models.Model):
    rider = models.ForeignKey(User, on_delete=models.CASCADE, related_name='rides')
    pickup = models.CharField(max_length=255)
    drop = models.CharField(max_length=255)
    status = models.CharField(max_length=50, default='requested')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Ride {self.id} by {self.rider.username}"