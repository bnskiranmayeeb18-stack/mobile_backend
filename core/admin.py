from django.contrib import admin
from .models import VehicleType, Vehicle

# DriverProfile unte deeniki add chey, lekapothe ee 2 chalu
try:
    from .models import DriverProfile
    @admin.register(DriverProfile)
    class DriverProfileAdmin(admin.ModelAdmin):
        list_display = ('id', 'name', 'vehicle')
except:
    pass

@admin.register(VehicleType)
class VehicleTypeAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')

@admin.register(Vehicle)
class VehicleAdmin(admin.ModelAdmin):
    list_display = ('id', 'type', 'registration_number')