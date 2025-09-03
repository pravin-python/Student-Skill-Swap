from django.contrib import admin
from .models import Country , State , City , University , Department , Branch , UniversityImages , Level

@admin.register(Country)
class CountryAdmin(admin.ModelAdmin):
    list_display = ['name']
    verbose_name_plural = 'Countries'

@admin.register(State)
class StateAdmin(admin.ModelAdmin):
    list_display = ['name' , 'country']

@admin.register(City)
class CityAdmin(admin.ModelAdmin):
    list_display = ['name' , 'state']
    verbose_name_plural = 'Cities'

@admin.register(University)
class UniversityAdmin(admin.ModelAdmin):
    list_display = [
        'name',
        'image',
        'description',
        'established_year',
        'get_levels',
        'get_departments',  
        'country',
        'state',
        'city'
    ]
    verbose_name_plural = 'Universities'
  
    def get_departments(self, obj):
        return ", ".join([dept.name for dept in obj.departments.all()])
    get_departments.short_description = "Departments" 

    def get_levels(self, obj):
        return ", ".join([level.name for level in obj.levels.all()])
    get_levels.short_description = "Levels" 

@admin.register(Level)
class CityAdmin(admin.ModelAdmin):
    list_display = ['name']
    verbose_name_plural = 'Levels'

@admin.register(Department)
class DepartmentAdmin(admin.ModelAdmin):
    list_display = ['name' , 'description']
 
@admin.register(Branch)
class BranchAdmin(admin.ModelAdmin):
    list_display = ['name' , 'description' , 'department']

@admin.register(UniversityImages)
class UniversityImagesAdmin(admin.ModelAdmin):
    list_display = ['university' , 'image' , 'description']
    