from django.db import models

class Ride(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('ongoing', 'Ongoing'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
    ]

    customer = models.ForeignKey('auth.User', on_delete=models.CASCADE, null=True, blank=True)
    pickup_location = models.CharField(max_length=255, null=True, blank=True)
    drop_location = models.CharField(max_length=255, null=True, blank=True)
    driver_name = models.CharField(max_length=255, null=True, blank=True)
    fare = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)

    def __str__(self):
        return f"Ride {self.id} - {self.status}"