from django.db import models
from django.contrib.auth import get_user_model
from django.core.validators import MinValueValidator

User = get_user_model()


class DriverProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='driver_profile')
    is_online = models.BooleanField(default=False)
    current_lat = models.FloatField(null=True, blank=True)
    current_lng = models.FloatField(null=True, blank=True)
    last_location_update = models.DateTimeField(auto_now=True)

    def __str__(self): return f"Driver {self.user.id} - Online: {self.is_online}"


class Ride(models.Model):
    class Status(models.TextChoices):
        REQUESTED = 'REQUESTED', 'Requested'
        MATCHED = 'MATCHED', 'Matched'
        ACCEPTED = 'ACCEPTED', 'Accepted'
        STARTED = 'STARTED', 'Started'
        COMPLETED = 'COMPLETED', 'Completed'
        CANCELLED = 'CANCELLED', 'Cancelled'

    passenger = models.ForeignKey(User, on_delete=models.CASCADE, related_name='rides_as_passenger')
    driver = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='rides_as_driver')
    pickup_lat = models.FloatField(validators=[MinValueValidator(-90)])
    pickup_lng = models.FloatField(validators=[MinValueValidator(-180)])
    dest_lat = models.FloatField()
    dest_lng = models.FloatField()
    ride_type = models.CharField(max_length=20, default='STANDARD',
                                 choices=[('STANDARD', 'Standard'), ('PREMIUM', 'Premium')])
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.REQUESTED)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    version = models.IntegerField(default=0)  # For concurrent acceptance handling

    class Meta:
        indexes = [models.Index(fields=['status', 'created_at'])]

    def __str__(self): return f"Ride {self.id} - {self.status}"