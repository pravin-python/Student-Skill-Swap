from django.urls import path
from . import views

app_name = 'notifications'

urlpatterns = [
    path('get/', views.get_notifications, name='get_notifications'),
    path('mark_read/<int:notification_id>/', views.mark_as_read, name='mark_as_read'),
    path('mark_all_read/', views.mark_all_as_read, name='mark_all_as_read'),
]
