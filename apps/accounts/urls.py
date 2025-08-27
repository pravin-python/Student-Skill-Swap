from django.urls import path
from . import views

app_name = 'accounts'

urlpatterns = [
    path('register/',views.register,name="register"),
    path('login/',views.login_view,name="login"),
    path('logout/',views.logout_view,name='logout'),
    path("api/get-choices/", views.get_choices, name="get_choices"),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('profile/', views.profile, name='profile'),
    path('update-profile/', views.update_profile, name='update_profile'),
    path('change-password/', views.change_password, name='change_password'),
]