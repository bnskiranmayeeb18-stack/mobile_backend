from django.contrib import admin
from .models import MediaUpload

@admin.register(MediaUpload)
class MediaUploadAdmin(admin.ModelAdmin):
    list_display = ['file_name', 'user', 'state', 'file_size', 'created_at']
    list_filter = ['state', 'file_type']
    search_fields = ['file_name', 'idempotency_key']