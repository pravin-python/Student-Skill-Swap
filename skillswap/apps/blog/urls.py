from django.urls import path
from . import views

app_name = 'blog'

urlpatterns = [
    path('blogs/' ,views.BlogView , name="blogs"),
    path('blog-details/<int:pk>/' , views.BlogDetailView, name="blog-details"),
    path('myblogs/' , views.BlogProfileView , name="blog-profile-view"),
    path('add-blog/' , views.AddBlogView , name="add_blog"),
    path('blog/edit/<int:pk>' , views.BlogEditView , name="edit_blog"),
]