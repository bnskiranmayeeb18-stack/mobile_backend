from django.contrib import admin
from .models import DriverLocation

@admin.register(DriverLocation)
class DriverLocationAdmin(admin.ModelAdmin):
    list_display = ('driver', 'latitude', 'longitude', 'is_available', 'last_updated')
    list_filter = ('is_available',)