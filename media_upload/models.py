import uuid
from django.db import models
from django.conf import settings
from django.core.exceptions import ValidationError

class MediaUpload(models.Model):
    class State(models.TextChoices):
        SELECTED = 'SELECTED', 'Selected - File captured'
        STAGING = 'STAGING', 'Staging - Local ready'
        UPLOADING = 'UPLOADING', 'Uploading - In progress'
        UPLOADED = 'UPLOADED', 'Uploaded - Server received'
        PROCESSING = 'PROCESSING', 'Processing - Server side'
        PROCESSED = 'PROCESSED', 'Processed - Success'
        FAILED = 'FAILED', 'Failed'
        CANCELLED = 'CANCELLED', 'Cancelled'

    # Legal transitions map
    LEGAL_TRANSITIONS = {
        State.SELECTED: [State.STAGING, State.CANCELLED],
        State.STAGING: [State.UPLOADING, State.FAILED, State.CANCELLED],
        State.UPLOADING: [State.UPLOADED, State.FAILED, State.CANCELLED],
        State.UPLOADED: [State.PROCESSING, State.FAILED],
        State.PROCESSING: [State.PROCESSED, State.FAILED],
        State.FAILED: [State.UPLOADING, State.STAGING], # Retry allowed
        State.CANCELLED: [],
        State.PROCESSED: [],
    }

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='media_uploads')
    file_name = models.CharField(max_length=255)
    file_size = models.BigIntegerField(help_text="Bytes")
    file_type = models.CharField(max_length=100, help_text="mime type e.g. image/jpeg")
    state = models.CharField(max_length=20, choices=State.choices, default=State.SELECTED)
    idempotency_key = models.CharField(max_length=100, unique=True, db_index=True)
    correlation_id = models.UUIDField(default=uuid.uuid4, editable=False)
    error_message = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def clean(self):
        if self.file_size > 100 * 1024 * 1024: # 100 MB limit
            raise ValidationError("File size cannot exceed 100MB")

    def can_transition_to(self, new_state):
        return new_state in self.LEGAL_TRANSITIONS.get(self.state, [])

    def transition_to(self, new_state, error_msg=None):
        if not self.can_transition_to(new_state):
            raise ValidationError(f"Illegal transition from {self.state} to {new_state}")
        self.state = new_state
        if error_msg:
            self.error_message = error_msg
        self.save()
        return self

    def __str__(self):
        return f"{self.file_name} [{self.state}]"

    class Meta:
        ordering = ['-created_at']