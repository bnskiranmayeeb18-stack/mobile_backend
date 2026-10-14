from django.db import models
from django.conf import settings

class SavedService(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='saved_services')
    service_name = models.CharField(max_length=255, db_index=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'service_name')
        # Django 5: constraints = [models.UniqueConstraint(fields=['user','service_name'], name='unique_user_service')]
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.user} - {self.service_name}"