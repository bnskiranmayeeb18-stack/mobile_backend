from django.db import models
from django.contrib.auth.models import User

class Ride(models.Model):
    customer = models.ForeignKey(User, on_delete=models.CASCADE, db_index=True)
    pickup_location = models.CharField(max_length=255)
    drop_location = models.CharField(max_length=255)
    fare = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)

    class Meta:
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['customer', 'created_at']),
        ]

    def __str__(self):
        return f"Ride {self.id} - {self.customer.username}"

# --- NEW EPIC 04 TASK 1 ---
class DriverLocation(models.Model):
    driver = models.ForeignKey(User, on_delete=models.CASCADE, related_name='locations', db_index=True)
    latitude = models.DecimalField(max_digits=9, decimal_places=6, help_text="Latitude -90 to 90")
    longitude = models.DecimalField(max_digits=9, decimal_places=6, help_text="Longitude -180 to 180")
    accuracy = models.FloatField(null=True, blank=True, help_text="Accuracy in meters")
    updated_at = models.DateTimeField(auto_now=True, db_index=True)

    class Meta:
        ordering = ['-updated_at']
        indexes = [
            models.Index(fields=['latitude', 'longitude']),
            models.Index(fields=['driver', 'updated_at']),
        ]

    def __str__(self):
        return f"Driver {self.driver_id} - ({self.latitude}, {self.longitude})"