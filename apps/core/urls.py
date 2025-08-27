from django.urls import path
from . import views

app_name = 'core'

urlpatterns = [
    path('',views.HomeView,name='home'),
    path('about/',views.AboutView,name="about"),
    path('contact/',views.ContactView,name="contact"),
    path('terms/',views.TermsView,name="terms"),
    path('privacy/',views.PrivacyView,name="privacy")
]

