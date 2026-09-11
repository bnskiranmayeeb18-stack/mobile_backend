from django.db import models
import uuid

class Ride(models.Model):
    STATUS_CHOICES = [
        ('REQUESTED', 'REQUESTED'),
        ('ACCEPTED', 'ACCEPTED'),
        ('DRIVER_ARRIVING', 'DRIVER_ARRIVING'),
        ('STARTED', 'STARTED'),
        ('COMPLETED', 'COMPLETED'),
        ('CANCELLED', 'CANCELLED'),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    # Basic ride info
    passenger_id = models.CharField(max_length=100, default='passenger_123')
    driver_id = models.CharField(max_length=100, null=True, blank=True)

    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='REQUESTED')

    # Pickup and Drop
    pickup_lat = models.FloatField(default=17.7231)
    pickup_lng = models.FloatField(default=83.3012)
    drop_lat = models.FloatField(default=17.7300)
    drop_lng = models.FloatField(default=83.3200)

    # Driver Live Location - Task 5 kosam
    driver_lat = models.FloatField(null=True, blank=True)
    driver_lng = models.FloatField(null=True, blank=True)
    driver_heading = models.FloatField(null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.id} - {self.status}"