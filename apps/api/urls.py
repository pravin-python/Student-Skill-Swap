from django.urls import path
from .views import HomeAPICoursesView , HomeAPIInstructorView , BlogAPIView

app_name = 'api'

urlpatterns = [
   path("api/courses/", HomeAPICoursesView.as_view(), name="home-courses-api"),
   path("api/instructors/" , HomeAPIInstructorView.as_view(), name="home-instructors-api" ),
   path("api/blogs/" , BlogAPIView.as_view() , name="blog-api"),
]