from django.urls import path
from . import views

app_name = 'university'

urlpatterns = [
    path('', views.UniversityView, name='university'), 
    path("<str:name>/", views.UniversityDetailView, name="university_detail"),
]


