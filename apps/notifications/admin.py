from django.contrib import admin
from .models import Notification

@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = ('recipient', 'notification_type', 'title', 'is_read', 'created_at')
    list_filter = ('notification_type', 'is_read', 'created_at')
    search_fields = ('recipient__username', 'recipient__first_name', 'recipient__last_name', 'title', 'message')
    readonly_fields = ('created_at',)
    list_per_page = 50
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('recipient', 'notification_type', 'title', 'message')
        }),
        ('Status', {
            'fields': ('is_read', 'created_at')
        }),
        ('Related Content', {
            'fields': ('content_type', 'object_id', 'data'),
            'classes': ('collapse',)
        }),
    )
