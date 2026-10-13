from django.db import models
class Notification(models.Model):
    user = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    message = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)