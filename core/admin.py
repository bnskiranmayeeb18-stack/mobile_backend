from django.contrib import admin
from .models import Ride, DriverLocation

@admin.register(Ride)
class RideAdmin(admin.ModelAdmin):
    list_display = ['id', 'customer', 'fare', 'created_at']
    list_filter = ['created_at']
    search_fields = ['customer__username']

@admin.register(DriverLocation)
class DriverLocationAdmin(admin.ModelAdmin):
    list_display = ['id', 'driver', 'latitude', 'longitude', 'accuracy', 'updated_at']
    list_filter = ['updated_at']