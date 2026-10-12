from django.db import models
from django.conf import settings
import os

def profile_upload_path(instance, filename):
    ext = filename.split('.')[-1].lower()
    return f'profiles/user_{instance.user.id}.{ext}'

class UserProfile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='userprofile')
    image = models.ImageField(upload_to=profile_upload_path, null=True, blank=True)
    bio = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Profile {self.user.username}"
