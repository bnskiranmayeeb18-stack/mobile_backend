from django.db import models
import uuid

class Media(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    file_name = models.CharField(max_length=255)
    status = models.CharField(max_length=20, default='PENDING') # PENDING, PROCESSING, COMPLETED, FAILED
    size = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.id} - {self.status}"

class ProcessedEvent(models.Model):
    event_id = models.CharField(max_length=255, unique=True, db_index=True)
    media_id = models.CharField(max_length=255, db_index=True)
    event_type = models.CharField(max_length=50)
    status = models.CharField(max_length=50)
    result = models.JSONField(null=True, blank=True)
    correlation_id = models.CharField(max_length=255, null=True, blank=True)
    processed_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        indexes = [
            models.Index(fields=['media_id', 'event_type']),
        ]

    def __str__(self):
        return f"{self.event_id} - {self.event_type}"
