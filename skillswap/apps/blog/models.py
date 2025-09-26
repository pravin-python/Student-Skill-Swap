from django.db import models
from apps.accounts.models import User
from apps.category_skills.models import SkillsCategory
import os
from ckeditor.fields import RichTextField  
from django.utils.text import slugify

def blog_images(instance,filename):
    return os.path.join('blog_images/',instance.author.username,filename)

class Blog(models.Model):

    class Meta:
        db_table = "blogs"
        ordering = ['-created_at']

    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name="blogs")
    title = models.CharField(max_length=255)
    category = models.ForeignKey(SkillsCategory,on_delete=models.SET_NULL,related_name="blogs" , null=True , default="Business")
    intro = RichTextField(blank=True, null=True)  
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_published = models.BooleanField(default=True)

    def __str__(self):
        return self.title

def blog_section_images(instance , filename):
    safe_title = slugify(instance.blog.title)  
    return os.path.join('blog_section/',safe_title , filename)

class BlogSection(models.Model):

    class Meta:
        db_table = 'blogs_section'
        ordering = ['-created_at']

    blog = models.ForeignKey(Blog, on_delete=models.CASCADE, related_name="sections")
    title = models.CharField(max_length=255)
    content = RichTextField(blank=True, null=True)
    images = models.ImageField(upload_to=blog_section_images) 
    order = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.title} ({self.blog.title})"

class BlogImages(models.Model):
    class Meta:
        db_table = 'blogs_images'
        ordering = ['-created_at']

    blog = models.ForeignKey(Blog , on_delete=models.CASCADE, related_name="images")
    image = models.ImageField(upload_to='blogs_images/')
    base = models.BooleanField(default=False)
    thumbnail = models.BooleanField(default=False)
    small = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.image} ({self.blog.title})"