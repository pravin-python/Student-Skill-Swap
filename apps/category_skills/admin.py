from django.contrib import admin
from .models import SkillsCategory , Skills

@admin.register(SkillsCategory)
class SkillsCategoryAdmin(admin.ModelAdmin):
    list_display = ['name' , 'description' , 'image']
    

@admin.register(Skills)
class SkillsAdmin(admin.ModelAdmin):
    list_display = ['name', 'category' , 'image' , 'description']
