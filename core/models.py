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
    class Status(models.TextChoices):
        REQUESTED = 'REQUESTED', 'Requested'
        ACCEPTED = 'ACCEPTED', 'Accepted'
        DRIVER_ARRIVING = 'DRIVER_ARRIVING', 'Driver Arriving'
        STARTED = 'STARTED', 'Started'
        COMPLETED = 'COMPLETED', 'Completed'
        CANCELLED = 'CANCELLED', 'Cancelled'

    STATUS_TRANSITIONS = {
        'REQUESTED': ['ACCEPTED', 'CANCELLED'],
        'ACCEPTED': ['DRIVER_ARRIVING', 'CANCELLED'],
        'DRIVER_ARRIVING': ['STARTED'],
        'STARTED': ['COMPLETED'],
        'COMPLETED': [],
        'CANCELLED': [],
    }

    RIDE_TYPES = [('standard','standard'),('premium','premium'),('shared','shared')]

    customer_name = models.CharField(max_length=100)
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.REQUESTED)
    driver = models.ForeignKey(DriverProfile, null=True, blank=True, on_delete=models.SET_NULL, related_name='rides')
    pickup_location = models.CharField(max_length=255, default="Unknown")
    drop_location = models.CharField(max_length=255, default="Unknown")
    ride_type = models.CharField(max_length=20, choices=RIDE_TYPES, default='standard')
    passenger_info = models.JSONField(default=dict, blank=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True)

    def can_transition_to(self, new_status):
        return new_status in self.STATUS_TRANSITIONS.get(self.status, [])

    def __str__(self):
        return f"{self.customer_name} - {self.status}"