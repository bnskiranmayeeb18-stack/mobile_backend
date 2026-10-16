from django.contrib import admin
from .models import MediaAsset

@admin.register(MediaAsset)
class MediaAssetAdmin(admin.ModelAdmin):
    list_display = ("id", "owner", "original_filename", "processing_status", "created_at", "correlation_id")
    list_filter = ("processing_status", "mime_type")
    search_fields = ("original_filename", "id", "owner__email")
    readonly_fields = ("id", "created_at", "updated_at")
