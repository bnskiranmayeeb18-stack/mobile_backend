import uuid
from django.db import models
from django.conf import settings

def safe_upload_path(instance, filename):
    folder = "public" if instance.is_public else "private"
    return f"media/{folder}/{filename}"

class MediaFile(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='media_files')
    file = models.FileField(upload_to=safe_upload_path)
    original_name = models.CharField(max_length=255)
    safe_name = models.CharField(max_length=255, blank=True)
    mime_type = models.CharField(max_length=100)
    file_size = models.PositiveIntegerField()
    width = models.PositiveIntegerField(null=True)
    height = models.PositiveIntegerField(null=True)
    sha256 = models.CharField(max_length=64, db_index=True, blank=True)
    is_public = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']
        indexes = [models.Index(fields=['user', 'is_public'])]

    def __str__(self):
        return f"{self.original_name} - {self.user_id}"
