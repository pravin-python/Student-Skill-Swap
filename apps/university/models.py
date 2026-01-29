from django.db import models
import os
from django.utils.text import slugify

class Country(models.Model):
    class Meta:
        ordering = ['name']
        db_table = 'countries'
        verbose_name_plural = 'Countries'

    name = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name    


class State(models.Model):
    class Meta:
        ordering = ['name']
        unique_together = ['name', 'country']
        db_table = 'states'

    name = models.CharField(max_length=100)
    country = models.ForeignKey(Country, on_delete=models.CASCADE, related_name='states')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.name


class City(models.Model):
    class Meta:
        unique_together = ['name', 'state']
        db_table = 'cities'
        verbose_name_plural = 'Cities'

    name = models.CharField(max_length=100)
    state = models.ForeignKey(State, on_delete=models.CASCADE, related_name='cities')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.name


class Department(models.Model):
    class Meta:
        ordering = ['name']
        db_table = 'department'
        
    name = models.CharField(max_length=100, unique=True, help_text="Enter Full Department Name")
    description = models.TextField(blank=True, help_text="Brief description of the department")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
   
    def __str__(self):
        return self.name


class Branch(models.Model):
    class Meta:
        ordering = ['name']
        unique_together = ['department', 'name']
        db_table = 'branch'
        verbose_name_plural = 'Branches'

    name = models.CharField(max_length=100)
    department = models.ForeignKey(Department, on_delete=models.CASCADE, related_name='branches')
    description = models.TextField(blank=True, help_text="Brief description of the branch")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.name

class Level(models.Model):
    class Meta:
        ordering = ['name']
        db_table = 'levels'
        verbose_name_plural = 'Levels'

    name = models.CharField(max_length=100, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

class University(models.Model):
    class Meta:
        ordering = ['name']
        verbose_name_plural = 'Universities'
        unique_together = ['name', 'city']
        db_table = 'universities'

    name = models.CharField(unique=True, max_length=100)
    slug = models.SlugField(max_length=255,unique=True)
    image = models.ImageField(upload_to='universities_icon/')
    description = models.TextField(max_length=999, help_text="Enter description for your university")
    established_year = models.PositiveIntegerField()
    departments = models.ManyToManyField(Department, related_name="universities")
    levels = models.ManyToManyField(Level, related_name="universities")  # ✅ Many-to-Many
    country = models.ForeignKey(Country, on_delete=models.SET_NULL, null=True, related_name='university_country')
    state = models.ForeignKey(State, on_delete=models.SET_NULL, null=True, related_name='university_state')
    city = models.ForeignKey(City, on_delete=models.SET_NULL, null=True, related_name="university_city")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        # Generate slug only if it doesn't exist
        if not self.slug:
            base_slug = slugify(self.name)
            slug = base_slug
            counter = 1

            # Ensure slug is unique
            while University.objects.filter(slug=slug).exists():
                slug = f"{base_slug}-{counter}"
                counter += 1
            
            self.slug = slug

        super().save(*args, **kwargs)

def university_upload_to(instance, filename):
    return os.path.join('universities_images', instance.university.name, filename)


class UniversityImages(models.Model):
    class Meta:
        ordering = ['-updated_at']
        verbose_name_plural = 'Universities_Images'
        db_table = 'university_images'

    image = models.ImageField(upload_to=university_upload_to)
    description = models.TextField(max_length=999, help_text="Enter Description for the image")
    university = models.ForeignKey(University, on_delete=models.CASCADE, related_name='images')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
