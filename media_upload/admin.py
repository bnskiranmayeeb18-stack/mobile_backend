from django.contrib import admin
from .models import Media, ProcessedEvent

@admin.register(Media)
class MediaAdmin(admin.ModelAdmin):
    list_display = ['id', 'file_name', 'status', 'size', 'created_at']
    list_filter = ['status']
    search_fields = ['file_name', 'id']

@admin.register(ProcessedEvent)
class ProcessedEventAdmin(admin.ModelAdmin):
    list_display = ['event_id', 'media_id', 'event_type', 'status', 'processed_at']
    list_filter = ['event_type', 'status']
    search_fields = ['event_id', 'media_id']
    readonly_fields = ['processed_at']
