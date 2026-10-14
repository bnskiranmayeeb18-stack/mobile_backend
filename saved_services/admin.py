from django.contrib import admin
from .models import SavedService

@admin.register(SavedService)
class SavedServiceAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'service_name', 'created_at')