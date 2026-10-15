from django.contrib import admin
from .models import Ride

@admin.register(Ride)
class RideAdmin(admin.ModelAdmin):
    list_display = ('id', 'rider', 'pickup', 'drop', 'status', 'created_at')
    list_filter = ('status',)
    search_fields = ('pickup', 'drop')

# keep Booking alias for old code
try:
    Booking = Ride
except:
    pass
