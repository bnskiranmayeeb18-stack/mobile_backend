from django.contrib import admin
from .models import Booking

@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ['id', 'customer', 'provider', 'service_name', 'status', 'amount', 'created_at']
    list_filter = ['status', 'created_at']
    search_fields = ['service_name', 'idempotency_key']
    readonly_fields = ['id', 'created_at', 'updated_at']