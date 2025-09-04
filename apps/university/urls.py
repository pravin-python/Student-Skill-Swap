from django.urls import path
from . import views

app_name = 'university'

urlpatterns = [
    path('', views.UniversityView, name='university'), 
    path("<int:university_id>/", views.UniversityDetailView, name="university_detail"),
]


