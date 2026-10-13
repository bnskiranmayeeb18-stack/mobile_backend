import uuid
from django.db import models
from django.contrib.auth.models import User

def service_image_path(instance, filename):
    return f"services/{filename}"
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
# Booking model lo add chey:
class Booking(models.Model):
    class Status(models.TextChoices):
        PENDING = 'PENDING', 'Pending'
        CONFIRMED = 'CONFIRMED', 'Confirmed'
        IN_PROGRESS = 'IN_PROGRESS', 'In Progress'
        COMPLETED = 'COMPLETED', 'Completed'
        CANCELLED = 'CANCELLED', 'Cancelled'
        PAYMENT_FAILED = 'PAYMENT_FAILED', 'Payment Failed'

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='bookings')
    ride = models.ForeignKey(Ride, on_delete=models.CASCADE, related_name='bookings', null=True)
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.PENDING)
    created_at = models.DateTimeField(auto_now_add=True)

    VALID_TRANSITIONS = {
        'PENDING': ['CONFIRMED', 'CANCELLED', 'PAYMENT_FAILED'],
        'CONFIRMED': ['IN_PROGRESS', 'CANCELLED'],
        'IN_PROGRESS': ['COMPLETED', 'CANCELLED'],
        'COMPLETED': [], 'CANCELLED': [], 'PAYMENT_FAILED': [],
    }

    def can_transition(self, new_status):
        return new_status in self.VALID_TRANSITIONS.get(self.status, [])

    def update_status(self, new_status):
        if not self.can_transition(new_status):
            raise ValueError(f"Invalid transition {self.status} -> {new_status}")
        self.status = new_status
        self.save()