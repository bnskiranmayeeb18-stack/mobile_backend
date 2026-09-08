from django.db import models
from django.contrib.auth.models import User

class Ride(models.Model):
    customer = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True, db_index=True)
    pickup_location = models.CharField(max_length=255, null=True, blank=True)
    drop_location = models.CharField(max_length=255, null=True, blank=True)
    fare = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    status = models.CharField(max_length=20, default='pending')
    created_at = models.DateTimeField(auto_now_add=True, null=True, db_index=True)

    class Meta:
        indexes = [
            models.Index(fields=['customer', 'created_at']),
        ]
        ordering = ['-created_at']

    def __str__(self):
        return f"Ride {self.id} - {self.status}"