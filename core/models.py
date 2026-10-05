import uuid
from django.db import models


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
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.id} - {self.status}"