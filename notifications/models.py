from django.db import models

class Notification(models.Model):
    ride_id = models.IntegerField()
    event_type = models.CharField(max_length=50, default='ride_completed')
    message = models.TextField(default='test message')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('ride_id', 'event_type')
        ordering = ['-created_at']

    def __str__(self):
        return f"Ride {self.ride_id} - {self.event_type}"