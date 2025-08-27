from django.contrib import admin
from .models import User

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ['first_name' , 'last_name' , 'gender' , 'profile_pic' , 'university_name' , 'personal_email' , 'department' , 'branch' , 'year' , 'bio' , 'created_at' , 'updated_at']
    verbose_name_plural = "Users"