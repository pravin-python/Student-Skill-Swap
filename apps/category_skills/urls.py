from django.urls import path
from . import views

app_name = 'category_skills'

urlpatterns = [
    # Course related URLs
    path('' , views.CourseView , name="courses"),
    path('course_details/<int:skill_id>/' , views.CourseDetailView , name="course_details"),
    path('instructors/', views.InstructorView , name="instructors"),
    path('add_skill/<int:skill_id>/', views.add_skill_to_profile, name="add_skill"),
    path('remove_skill/<int:skill_id>/', views.remove_skill_from_profile, name="remove_skill"),
    
    # Request management URLs
    path('send_request/', views.send_request, name="send_request"),
    path('requests/', views.request_management, name="requests"),
    path('accept_request/<int:request_id>/', views.accept_request, name="accept_request"),
    path('reject_request/<int:request_id>/', views.reject_request, name="reject_request"),
    path('cancel_request/<int:request_id>/', views.cancel_request, name="cancel_request"),
    path('delete_request/<int:request_id>/', views.delete_request, name="delete_request"),
    
    # Session management URLs
    path('sessions/', views.session_management, name="sessions"),
    path('create_session/', views.create_session, name="create_session"),
    path('start_session/<int:session_id>/', views.start_session, name="start_session"),
    path('complete_session/<int:session_id>/', views.complete_session, name="complete_session"),
    path('cancel_session/<int:session_id>/', views.cancel_session, name="cancel_session"),
    path('delete_session/<int:session_id>/', views.delete_session, name="delete_session"),
]