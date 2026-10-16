from django.db import models
from django.conf import settings
from django.utils import timezone
import datetime

def get_default_expiry():
    return timezone.now() + datetime.timedelta(hours=24)

class IdempotencyKey(models.Model):
    key = models.CharField(max_length=255, unique=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True, blank=True)
    method = models.CharField(max_length=10, default='POST')
    path = models.CharField(max_length=500, blank=True)
    request_hash = models.CharField(max_length=64, blank=True)
    response_status = models.IntegerField(null=True, blank=True)
    response_body = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField(default=get_default_expiry)

    class Meta:
        indexes = [
            models.Index(fields=['key']),
            models.Index(fields=['expires_at']),
        ]

    def __str__(self):
        return f"{self.key} - {self.expires_at}"