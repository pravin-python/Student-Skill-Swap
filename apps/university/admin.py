from django.contrib import admin
from .models import Country , State , City , University , Department , Branch , UniversityImages

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
    list_display = ['name' , 'image' , 'description' , 'established_year' , 'country' , 'state' , 'city']
    verbose_name_plural = 'Universities'

@admin.register(Department)
class DepartmentAdmin(admin.ModelAdmin):
    list_display = ['name' , 'description']
 
@admin.register(Branch)
class BranchAdmin(admin.ModelAdmin):
    list_display = ['name' , 'description' , 'department']

@admin.register(UniversityImages)
class UniversityImagesAdmin(admin.ModelAdmin):
    list_display = ['university' , 'image' , 'description']
    