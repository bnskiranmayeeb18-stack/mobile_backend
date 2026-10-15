from django.contrib import admin
from .models import Booking

@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ('id', 'rider', 'status', 'created_at', 'updated_at')
    list_filter = ('status',)
    readonly_fields = ('created_at', 'updated_at')
