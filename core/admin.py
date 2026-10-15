from django.contrib import admin
from .models import IdempotencyKey

@admin.register(IdempotencyKey)
class IdempotencyKeyAdmin(admin.ModelAdmin):
    list_display = ('key', 'user', 'method', 'path', 'created_at', 'expires_at')
    list_filter = ('method',)
    search_fields = ('key', 'user__username')
