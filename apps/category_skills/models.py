from django.db import models
import os

class SkillsCategory(models.Model):

    class Meta:
        ordering = ['name']
        db_table = 'category'
        verbose_name_plural = "Skill Categories"

    name = models.CharField(max_length=25,unique=True)
    description = models.TextField(max_length=999,help_text="Enter Description For Particular Course")
    image = models.ImageField(upload_to='category/' , blank=True , null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name    

def category_skills(instance , filename):
        return os.path.join('category_skills', instance.category.name, filename)


class Skills(models.Model):

    class Meta:
        ordering = ['category' , 'name']
        db_table = 'category_skills'
        unique_together = ['name','category']
        verbose_name_plural = 'Skills'
    
    name = models.CharField(max_length=200,unique=True)
    category = models.ForeignKey(SkillsCategory,on_delete=models.CASCADE,related_name='skills')
    image = models.ImageField(upload_to=category_skills,blank=True,null=True)
    description = models.TextField(max_length=999,help_text="Enter Description for Specific Skill") 
    created_at = models.DateField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name    
