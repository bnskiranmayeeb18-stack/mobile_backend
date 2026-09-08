from django.db import models
from django.contrib.auth.models import User

class DriverLocation(models.Model):
    driver = models.OneToOneField(User, on_delete=models.CASCADE)
    latitude = models.FloatField()
    longitude = models.FloatField()
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.driver.username} - {self.latitude}, {self.longitude}"