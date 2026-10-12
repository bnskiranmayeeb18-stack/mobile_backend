from django.db import models
from django.conf import settings

def profile_path(instance, filename):
    return f"profiles/{instance.user.id}/{filename}"

class Profile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='profile')
    image = models.ImageField(upload_to=profile_path, null=True, blank=True)
    bio = models.TextField(blank=True)

    def __str__(self):
        return f"{self.user.email} Profile"