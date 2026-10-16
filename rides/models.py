from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.db import IntegrityError

class Ride(models.Model):
    STATUS_CHOICES = [
        ('requested', 'requested'),
        ('accepted', 'accepted'),
        ('started', 'started'),
        ('completed', 'completed'),
        ('cancelled', 'cancelled'),
    ]
    rider = models.ForeignKey(User, on_delete=models.CASCADE, related_name='rides', null=False, blank=False)
    driver = models.ForeignKey(User, on_delete=models.CASCADE, related_name='driven_rides', null=True, blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_rides', null=True, blank=True)
    pickup = models.CharField(max_length=255)
    drop = models.CharField(max_length=255)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='requested')
    idempotency_key = models.CharField(max_length=255, null=True, blank=True)
    version = models.IntegerField(default=1)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-updated_at', '-id']

    def full_clean(self, *args, **kwargs):
        if self.rider is None:
            raise ValidationError({"rider": "rider is required"})
        super().full_clean(*args, **kwargs)

    def save(self, *args, **kwargs):
        if self.rider is None:
            raise IntegrityError("rider_id may not be NULL")
        if self.pk:
            self.version = self.version + 1
        super().save(*args, **kwargs)

class Booking(Ride):
    class Meta:
        proxy = True

class IdempotencyKey(models.Model):
    key = models.CharField(max_length=128)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='idempotency_keys')
    method = models.CharField(max_length=10)
    path = models.CharField(max_length=512)
    body_hash = models.CharField(max_length=64)
    response_code = models.IntegerField(null=True, blank=True)
    response_body = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        unique_together = ('user', 'key')
class BookingStatus:
    PENDING = 'pending'
    CONFIRMED = 'confirmed'
    IN_PROGRESS = 'in_progress'
    COMPLETED = 'completed'
    CANCELLED = 'cancelled'

# Alias for tests expecting Booking
Booking = Ride