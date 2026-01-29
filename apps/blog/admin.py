from django.contrib import admin
from .models import Blog, BlogSection , BlogImages

@admin.register(Blog)
class BlogAdmin(admin.ModelAdmin):
    list_display = ("title", "author", "created_at", "updated_at", "is_published")
    search_fields = ("title", "author__first_name", "author__last_name")
    readonly_fields = ("created_at", "updated_at")
    verbose_name_plural = "Blogs"

@admin.register(BlogSection)
class BlogSectionAdmin(admin.ModelAdmin):
    list_display = ("title", "blog", "order", "content" , "images")
    search_fields = ("title", "blog__title")
    readonly_fields = ("created_at", "updated_at")
    verbose_name_plural = "Blogs_Section"

@admin.register(BlogImages)
class BlogImagesAdmin(admin.ModelAdmin):
    list_display = ('blog', 'image', 'base', 'thumbnail', 'small', 'created_at')
    list_filter = ('base', 'thumbnail', 'small', 'created_at')
    search_fields = ('blog__title',)
    readonly_fields = ('created_at', 'updated_at')
    verbose_name_plural = "Blogs_Image"