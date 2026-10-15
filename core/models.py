from django.db import models
from django.contrib.auth import get_user_model
from django.utils import timezone
import datetime

User = get_user_model()

class IdempotencyKey(models.Model):
    key = models.CharField(max_length=128)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    method = models.CharField(max_length=10)
    path = models.CharField(max_length=512)
    request_hash = models.CharField(max_length=64)
    response_status = models.IntegerField()
    response_body = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField(default=lambda: timezone.now() + datetime.timedelta(hours=24))

    class Meta:
        unique_together = ('key', 'user')
        indexes = [
            models.Index(fields=['key', 'user']),
            models.Index(fields=['expires_at']),
        ]

    def is_expired(self):
        return timezone.now() > self.expires_at
