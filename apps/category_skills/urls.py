from django.urls import path
from . import views

app_name = 'category_skills'

urlpatterns = [
    path('' , views.CourseView , name="courses"),
    path('courses_detail/' , views.CourseDetailView , name="course_details"),
    path('instructors/', views.InstructorView , name="instructors")
]