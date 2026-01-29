from django.contrib import admin
from .models import SkillsCategory , Skills, UserSkills, Request, Session

@admin.register(SkillsCategory)
class SkillsCategoryAdmin(admin.ModelAdmin):
    list_display = ['name' , 'description' , 'icon_class','image']
    

@admin.register(Skills)
class SkillsAdmin(admin.ModelAdmin):
    list_display = ['name', 'category' , 'image' , 'description' , 'level']


@admin.register(UserSkills)
class UserSkillsAdmin(admin.ModelAdmin):
    list_display = ['user', 'skill', 'added_at' , 'is_favourite']
    list_filter = ['skill__category', 'added_at']
    search_fields = ['user__username', 'user__first_name', 'user__last_name', 'skill__name']
    date_hierarchy = 'added_at'


@admin.register(Request)
class RequestAdmin(admin.ModelAdmin):
    list_display = ['requester', 'receiver', 'skill', 'status', 'created_at', 'responded_at']
    list_filter = ['status', 'skill__category', 'created_at', 'responded_at']
    search_fields = ['requester__username', 'receiver__username', 'skill__name', 'description']
    date_hierarchy = 'created_at'
    readonly_fields = ['created_at', 'updated_at']
    
    fieldsets = (
        ('Request Information', {
            'fields': ('requester', 'receiver', 'skill', 'status')
        }),
        ('Message', {
            'fields': ('description',)
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at', 'responded_at'),
            'classes': ('collapse',)
        }),
    )


@admin.register(Session)
class SessionAdmin(admin.ModelAdmin):
    list_display = ['title', 'teacher', 'learner', 'skill', 'status', 'scheduled_date', 'duration_minutes']
    list_filter = ['status', 'session_type', 'skill__category', 'scheduled_date', 'created_at']
    search_fields = ['title', 'teacher__username', 'learner__username', 'skill__name', 'description']
    date_hierarchy = 'scheduled_date'
    readonly_fields = ['created_at', 'updated_at', 'completed_at']
    
    fieldsets = (
        ('Session Information', {
            'fields': ('title', 'teacher', 'learner', 'skill', 'request')
        }),
        ('Schedule & Location', {
            'fields': ('scheduled_date', 'duration_minutes', 'session_type', 'location')
        }),
        ('Details', {
            'fields': ('description', 'status')
        }),
        ('Feedback', {
            'fields': ('teacher_rating', 'teacher_feedback', 'learner_rating', 'learner_feedback'),
            'classes': ('collapse',)
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at', 'completed_at'),
            'classes': ('collapse',)
        }),
    )
