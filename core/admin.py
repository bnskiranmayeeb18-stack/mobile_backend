from django.contrib import admin
from .models import VehicleType, DriverProfile, Vehicle, Ride, RideLocation

@admin.register(VehicleType)
class VehicleTypeAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'description', 'created_at')
    search_fields = ('name',)
    ordering = ('name',)

@admin.register(DriverProfile)
class DriverProfileAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'license_number', 'created_at')
    search_fields = ('license_number', 'user__username')
    list_filter = ('created_at',)
    ordering = ('-created_at',)

@admin.register(Vehicle)
class VehicleAdmin(admin.ModelAdmin):
    list_display = ('id', 'driver', 'vehicle_type', 'vehicle_number', 'created_at')
    search_fields = ('vehicle_number',)
    list_filter = ('vehicle_type',)
    ordering = ('-created_at',)

@admin.register(Ride)
class RideAdmin(admin.ModelAdmin):
    list_display = ('id', 'rider', 'driver', 'vehicle', 'status', 'fare', 'created_at')
    search_fields = ('rider__username', 'pickup_location', 'drop_location')
    list_filter = ('status', 'created_at')
    ordering = ('-created_at',)

@admin.register(RideLocation)
class RideLocationAdmin(admin.ModelAdmin):
    list_display = ('id', 'ride', 'pickup_lat', 'pickup_lng', 'drop_lat', 'drop_lng')
    search_fields = ('ride__id',)
    ordering = ('-created_at',)