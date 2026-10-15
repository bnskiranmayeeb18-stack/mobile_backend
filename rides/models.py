from django.db import models
from django.contrib.auth import get_user_model
from django.utils import timezone

User = get_user_model()

class Ride(models.Model):
    STATUS_CHOICES = [
        ('requested', 'Requested'),
        ('accepted', 'Accepted'),
        ('started', 'Started'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
    ]
    
    rider = models.ForeignKey(User, on_delete=models.CASCADE, related_name='rides')
    driver = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='driven_rides')
    pickup = models.CharField(max_length=255)
    drop = models.CharField(max_length=255)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='requested')
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)
    updated_at = models.DateTimeField(auto_now=True, db_index=True)
    version = models.IntegerField(default=1)
    idempotency_key = models.CharField(max_length=128, blank=True, db_index=True)

    def save(self, *args, **kwargs):
        if self.pk:
            self.version = self.version + 1
        super().save(*args, **kwargs)

    class Meta:
        ordering = ['-updated_at', '-id']

    def __str__(self):
        return f"Ride {self.id} - {self.status}"

class Booking(models.Model):
    # Backward compat - alias to Ride if needed
    rider = models.ForeignKey(User, on_delete=models.CASCADE, related_name='bookings')
    pickup = models.CharField(max_length=255, default='')
    drop = models.CharField(max_length=255, default='')
    status = models.CharField(max_length=20, default='requested')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-id']
