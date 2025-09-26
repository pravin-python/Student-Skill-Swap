from django.shortcuts import render, get_object_or_404 , redirect
from .models import SkillsCategory, Skills, UserSkills, Request, Session
from apps.accounts.models import User
from django.core.paginator import Paginator
from django.http import JsonResponse
from django.template.loader import render_to_string
from apps.accounts.views import login_required_custom
from django.utils import timezone
from django.db.models import Q
from apps.university.models import Department

def CourseView(request):
    categories = SkillsCategory.objects.all()
    user_id = request.session.get("user_id")

    # Get all users who have added skills
    users_with_skills = User.objects.filter(
        user_skills__isnull=False
    ).distinct().prefetch_related("user_skills__skill__category")

    if user_id:
        users_with_skills = users_with_skills.exclude(id=user_id)

    skills_qs = UserSkills.objects.filter(
        user__in=users_with_skills
    ).select_related("skill", "user", "skill__category")

    # --- Search filter ---
    search_query = request.GET.get("q")
    if search_query:
        skills_qs = skills_qs.filter(
            Q(skill__name__icontains=search_query) |  
            Q(user__first_name__icontains=search_query) |  
            Q(user__last_name__icontains=search_query)     
        ).distinct()

    # --- Category filter ---
    category_ids = request.GET.getlist("categories[]")
    if category_ids and "all" not in category_ids:
        skills_qs = skills_qs.filter(skill__category_id__in=category_ids)

    # --- Level filter ---
    level_filters = request.GET.getlist("levels[]")
    if level_filters and "all" not in level_filters:
        skills_qs = skills_qs.filter(skill__level__in=level_filters)

    # Pagination
    paginator = Paginator(skills_qs, 4)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    context = {
        "categories": categories,
        "level_choices": Skills.LEVEL_CHOICES,
        "page_obj": page_obj,
        "page_param": "page",
        "section": "courses",
    }

    # AJAX partial rendering
    if request.GET.get("ajax") == "1":
        html = render_to_string("category_skills/courses_grid.html", context, request=request)
        return JsonResponse({"html": html})

    return render(request, "category_skills/courses.html", context)
    
def CourseDetailView(request, username , name):

    user = get_object_or_404(User , username=username)

    skill = get_object_or_404(Skills, user_skills__user = user, slug=name)

    # Get the user who added this skill
    user_skill = get_object_or_404(UserSkills , user=user , skill = skill)

    return render(request, "category_skills/course-details.html", {
        "skill": skill,
        "user_skill": user_skill
    })

def InstructorView(request):
    # --- Base queryset: only users with skills ---
    users_with_skills = User.objects.filter(user_skills__isnull=False).distinct().prefetch_related(
        'user_skills__skill__category', 'department'
    )

    custom_user = request.session.get("user_id")
    # Exclude the logged-in user
    if custom_user:
        users_with_skills = users_with_skills.exclude(id=custom_user)

    # --- Search filter ---
    q = request.GET.get("q")
    if q:
        users_with_skills = users_with_skills.filter(
            Q(first_name__icontains=q) |
            Q(last_name__icontains=q) |
            Q(user_skills__skill__name__icontains=q)
        ).distinct()

    # --- Department filter ---
    categories = request.GET.getlist("categories[]")
    if categories and "all" not in categories:
        users_with_skills = users_with_skills.filter(department__id__in=categories).distinct()

    # --- Build instructor data ---
    instructors_data = []
    for user in users_with_skills:
        user_skills = user.user_skills.all()
        skills_list = [us.skill for us in user_skills]
        instructors_data.append({
            'user': user,
            'skills': skills_list,
            'skills_count': len(skills_list),
        })

    # --- Pagination ---
    paginator = Paginator(instructors_data, 6)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    departments = Department.objects.all()

    # Return JSON only for ajax=1 requests
    if request.GET.get("ajax") == "1":
        html = render_to_string("category_skills/instructors_grid.html", {
            "page_obj": page_obj,
            "section": "instructors",
            "page_param": "page"
        }, request=request)
        return JsonResponse({"html": html})

    # Otherwise return full HTML page
    return render(request, "category_skills/instructors.html", {
        "departments": departments,
        "page_obj": page_obj,
        "section": "instructors",
        "page_param": "page",
    })


def InstructorDetailView(request, username):
    user = get_object_or_404(
        User.objects.prefetch_related("user_skills__skill__category"),
        username=username
    )

    # Instructor’s skills
    skills_qs = Skills.objects.filter(user_skills__user=user).select_related("category").distinct()

    # Pagination (6 per page)
    paginator = Paginator(skills_qs, 4)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    # Instructor’s sessions (for Experience tab)
    sessions = Session.objects.filter(teacher=user).select_related("skill", "learner")

    # AJAX request → return only courses grid + pagination HTML
    if request.headers.get("x-requested-with") == "XMLHttpRequest":
        html = render_to_string(
            "category_skills/instructors_course_grid.html",
            {
                "page_obj": page_obj,
                "section": "courses",
                "page_param":"page"
            },
            request=request
        )
        return JsonResponse({"html": html})
    
    context = {
        "instructor": user,
        "skills": skills_qs,
        "page_obj": page_obj,      
        "skills_count": skills_qs.count(),
        "sessions": sessions,
        "section": "courses",
        "page_param": "page",
    }
    return render(request, "category_skills/instructor-profile.html", context)

@login_required_custom
def toggle_favourite(request, skill_id):
    """
    Toggle a skill as favourite for the logged-in user using the boolean field in UserSkills.
    """
    if request.method != 'POST':
        return JsonResponse({'success': False, 'message': 'Invalid request method!'})

    try:
        user_id = request.session.get('user_id')
        if not user_id:
            return JsonResponse({'success': False, 'message': 'Please Log in First!'})

        user = get_object_or_404(User, id=user_id)
        skill = get_object_or_404(Skills, id=skill_id)

        # Check if the user has this skill
        user_skill = UserSkills.objects.filter(user=user, skill=skill).first()
        if not user_skill:
            return JsonResponse({'success': False, 'message': 'You do not have this skill in your profile!'})

        # Toggle the favourite field
        user_skill.favourite = not user_skill.favourite
        user_skill.save()

        status = "added" if user_skill.favourite else "removed"
        message = f'Skill "{skill.name}" has been {status} to your favourites.'

        # Optional: create notification only when added
        from apps.notifications.views import create_notification
        if user_skill.favourite:
            create_notification(
                recipient=user,
                notification_type='favourite_added',
                title='Favourite Added',
                message=message,
                content_object=user_skill
            )

        return JsonResponse({'success': True, 'status': status, 'message': message})

    except Exception as e:
        print(f"Error in toggle_favourite: {str(e)}")
        return JsonResponse({'success': False, 'message': f'An error occurred: {str(e)}'})

@login_required_custom
def add_skill_to_profile(request, skill_id):
    """Add a skill to user's profile"""
    try:
        if request.method == 'POST':
            user_id = request.session.get('user_id')
            if not user_id:
                return JsonResponse({'success': False, 'message': 'User not logged in!'})
            
            user = get_object_or_404(User, id=user_id)
            skill = get_object_or_404(Skills, id=skill_id)
            
            # Check if skill is already added
            existing_user_skill = UserSkills.objects.filter(user=user, skill=skill).first()
            if existing_user_skill:
                return JsonResponse({'success': False, 'message': 'Skill already in your Profile!'})
            
            # Create new user skill
            user_skill = UserSkills.objects.create(user=user, skill=skill)
            
            # Create notification
            from apps.notifications.views import create_notification
            create_notification(
                recipient=user,
                notification_type='skill_added',
                title='Skill Added',
                message=f'Skill "{skill.name}" has been added to your profile successfully!',
                content_object=user_skill
            )
            
            return JsonResponse({'success': True, 'message': f'Skill "{skill.name}" added to your profile!'})
        else:
            return JsonResponse({'success': False, 'message': 'Invalid request method!'})
    except Exception as e:
        print(f"Error in add_skill_to_profile: {str(e)}")
        return JsonResponse({'success': False, 'message': f'An error occurred: {str(e)}'})

@login_required_custom
def remove_skill_from_profile(request, skill_id):
    """Remove a skill from user's profile"""
    try:
        if request.method == 'POST':
            user_id = request.session.get('user_id')
            if not user_id:
                return JsonResponse({'success': False, 'message': 'User not logged in!'})
            
            user = get_object_or_404(User, id=user_id)
            skill = get_object_or_404(Skills, id=skill_id)
            
            try:
                user_skill = UserSkills.objects.get(user=user, skill=skill)
                
                # Create notification before deletion
                from apps.notifications.views import create_notification
                create_notification(
                    recipient=user,
                    notification_type='skill_removed',
                    title='Skill Removed',
                    message=f'Skill "{skill.name}" has been removed from your profile.',
                    data={'skill_name': skill.name}
                )
                
                user_skill.delete()
                return JsonResponse({'success': True, 'message': f'Skill "{skill.name}" removed from your profile!'})
            except UserSkills.DoesNotExist:
                return JsonResponse({'success': False, 'message': 'Skill not found in your profile!'})
        else:
            return JsonResponse({'success': False, 'message': 'Invalid request method!'})
    except Exception as e:
        print(f"Error in remove_skill_from_profile: {str(e)}")
        return JsonResponse({'success': False, 'message': f'An error occurred: {str(e)}'})


# ============= REQUEST MANAGEMENT VIEWS =============

@login_required_custom
def send_request(request):
    """Send a skill learning request to another user"""
    if request.method == 'POST':
        try:
            user_id = request.session.get('user_id')
            requester = get_object_or_404(User, id=user_id)
            
            skill_id = request.POST.get('skill_id')
            receiver_id = request.POST.get('receiver_id')
            description = request.POST.get('description', '').strip()
            
            # Validation
            if not skill_id or not receiver_id or not description:
                return JsonResponse({'success': False, 'message': 'All fields are required.'})
            
            skill = get_object_or_404(Skills, id=skill_id)
            receiver = get_object_or_404(User, id=receiver_id)
            
            # Check if requester is trying to request from themselves
            if requester.id == receiver.id:
                return JsonResponse({'success': False, 'message': 'You cannot send a request to yourself.'})
            
            # Check if request already exists
            existing_request = Request.objects.filter(
                requester=requester,
                receiver=receiver,
                skill=skill,
                status__in=['P', 'A']  # Pending or Accepted
            ).first()
            
            if existing_request:
                status_msg = 'pending' if existing_request.status == 'P' else 'already accepted'
                return JsonResponse({'success': False, 'message': f'A request for this skill is {status_msg}.'})
            
            # Create new request
            new_request = Request.objects.create(
                requester=requester,
                receiver=receiver,
                skill=skill,
                description=description
            )
            
            # Create notification for receiver
            from apps.notifications.views import create_notification
            create_notification(
                recipient=receiver,
                notification_type='request_sent',
                title='New Learning Request',
                message=f'{requester.first_name} {requester.last_name} wants to learn {skill.name} from you.',
                content_object=new_request
            )
            
            return JsonResponse({
                'success': True, 
                'message': f'Request sent successfully to {receiver.first_name} {receiver.last_name}!'
            })
            
        except Exception as e:
            print(f"Error in send_request: {str(e)}")
            return JsonResponse({'success': False, 'message': f'An error occurred: {str(e)}'})
    
    return JsonResponse({'success': False, 'message': 'Invalid request method.'})


@login_required_custom
def request_management(request):
    """Request management page - view all requests"""
    user_id = request.session.get('user_id')
    user = get_object_or_404(User, id=user_id)

    # Get sent requests
    sent_requests = Request.objects.filter(requester=user).select_related(
        'receiver', 'skill', 'skill__category'
    ).order_by('-created_at')

    # Get received requests
    received_requests = Request.objects.filter(receiver=user).select_related(
        'requester', 'skill', 'skill__category'
    ).order_by('-created_at')

    # Stats
    total_sent = sent_requests.count()
    total_received = received_requests.count()
    pending_sent = sent_requests.filter(status='P').count()
    pending_received = received_requests.filter(status='P').count()
    accepted_sent = sent_requests.filter(status='A').count()
    accepted_received = received_requests.filter(status='A').count()

    # Sent Requests Pagination
    sent_paginator = Paginator(sent_requests, 4)
    sent_page_number = request.GET.get("sent_page")
    sent_page_obj = sent_paginator.get_page(sent_page_number)

    # Received Requests Pagination
    received_paginator = Paginator(received_requests, 4)
    received_page_number = request.GET.get("received_page")
    received_page_obj = received_paginator.get_page(received_page_number)

    context = {
        'custom_user': user,
        'sent_page_obj': sent_page_obj,
        'received_page_obj': received_page_obj,
        'stats': {
            'total_sent': total_sent,
            'total_received': total_received,
            'pending_sent': pending_sent,
            'pending_received': pending_received,
            'accepted_sent': accepted_sent,
            'accepted_received': accepted_received,
        }
    }

    if request.headers.get("x-requested-with") == "XMLHttpRequest":
        section = request.GET.get("section")
        if section == "received":
            html = render_to_string("category_skills/received_requests_grid.html", context, request=request)
        elif section == "sent":
            html = render_to_string("category_skills/sent_requests_grid.html", context, request=request)
        else:
            html = ""  # fallback
        return JsonResponse({"html": html})

    return render(request, 'category_skills/requests.html', context)



@login_required_custom
def accept_request(request, request_id):
    """Accept a skill learning request"""
    if request.method == 'POST':
        try:
            user_id = request.session.get('user_id')
            user = get_object_or_404(User, id=user_id)
            
            skill_request = get_object_or_404(Request, id=request_id, receiver=user)
            
            if skill_request.status != 'P':
                return JsonResponse({'success': False, 'message': 'This request has already been processed.'})
            
            # Accept the request
            skill_request.status = 'A'
            skill_request.responded_at = timezone.now()
            skill_request.save()
            
            # Create notification for requester
            from apps.notifications.views import create_notification
            create_notification(
                recipient=skill_request.requester,
                notification_type='request_accepted',
                title='Request Accepted',
                message=f'Your request to learn {skill_request.skill.name} from {user.first_name} {user.last_name} has been accepted!',
                content_object=skill_request
            )
            
            return JsonResponse({
                'success': True, 
                'message': f'Request from {skill_request.requester.first_name} accepted successfully!'
            })
            
        except Exception as e:
            print(f"Error in accept_request: {str(e)}")
            return JsonResponse({'success': False, 'message': f'An error occurred: {str(e)}'})
    
    return JsonResponse({'success': False, 'message': 'Invalid request method.'})


@login_required_custom
def reject_request(request, request_id):
    """Reject a skill learning request"""
    if request.method == 'POST':
        try:
            user_id = request.session.get('user_id')
            user = get_object_or_404(User, id=user_id)
            
            skill_request = get_object_or_404(Request, id=request_id, receiver=user)
            
            if skill_request.status != 'P':
                return JsonResponse({'success': False, 'message': 'This request has already been processed.'})
            
            # Get rejection reason
            reason = request.POST.get('reason', '').strip()
            if not reason:
                return JsonResponse({'success': False, 'message': 'Please provide a reason for rejection.'})
            
            # Reject the request
            skill_request.status = 'R'
            skill_request.responded_at = timezone.now()
            skill_request.save()
            
            # Create notification for requester
            from apps.notifications.views import create_notification
            create_notification(
                recipient=skill_request.requester,
                notification_type='request_rejected',
                title='Request Rejected',
                message=f'Your request to learn {skill_request.skill.name} from {user.first_name} {user.last_name} has been rejected. Reason: {reason}',
                content_object=skill_request,
                data={'reason': reason}
            )
            
            return JsonResponse({
                'success': True, 
                'message': f'Request from {skill_request.requester.first_name} rejected.'
            })
            
        except Exception as e:
            print(f"Error in reject_request: {str(e)}")
            return JsonResponse({'success': False, 'message': f'An error occurred: {str(e)}'})
    
    return JsonResponse({'success': False, 'message': 'Invalid request method.'})


@login_required_custom
def cancel_request(request, request_id):
    """Cancel a sent skill learning request"""
    if request.method == 'POST':
        try:
            user_id = request.session.get('user_id')
            user = get_object_or_404(User, id=user_id)
            
            skill_request = get_object_or_404(Request, id=request_id, requester=user)
            
            if skill_request.status != 'P':
                return JsonResponse({'success': False, 'message': 'Only pending requests can be cancelled.'})
            
            # Get cancellation reason
            reason = request.POST.get('reason', '').strip()
            if not reason:
                return JsonResponse({'success': False, 'message': 'Please provide a reason for cancellation.'})
            
            # Cancel the request
            skill_request.status = 'C'
            skill_request.save()
            
            # Create notification for receiver
            from apps.notifications.views import create_notification
            create_notification(
                recipient=skill_request.receiver,
                notification_type='request_cancelled',
                title='Request Cancelled',
                message=f'{user.first_name} {user.last_name} has cancelled their request to learn {skill_request.skill.name}. Reason: {reason}',
                content_object=skill_request,
                data={'reason': reason}
            )
            
            return JsonResponse({
                'success': True, 
                'message': 'Request cancelled successfully!'
            })
            
        except Exception as e:
            print(f"Error in cancel_request: {str(e)}")
            return JsonResponse({'success': False, 'message': f'An error occurred: {str(e)}'})
    
    return JsonResponse({'success': False, 'message': 'Invalid request method.'})


@login_required_custom
def delete_request(request, request_id):
    """Delete a request (soft delete by changing status)"""
    if request.method == 'POST':
        try:
            user_id = request.session.get('user_id')
            user = get_object_or_404(User, id=user_id)
            
            # Get request where user is either requester or receiver
            skill_request = Request.objects.filter(
                Q(requester=user) | Q(receiver=user),
                id=request_id
            ).first()
            
            if not skill_request:
                return JsonResponse({'success': False, 'message': 'Request not found or access denied.'})
            
            # Instead of actual deletion, we'll mark as cancelled/deleted
            skill_request.delete()  # Actual deletion for now, can be changed to soft delete if needed
            
            return JsonResponse({
                'success': True, 
                'message': 'Request deleted successfully!'
            })
            
        except Exception as e:
            print(f"Error in delete_request: {str(e)}")
            return JsonResponse({'success': False, 'message': f'An error occurred: {str(e)}'})
    
    return JsonResponse({'success': False, 'message': 'Invalid request method.'})


# ============= SESSION MANAGEMENT VIEWS =============

@login_required_custom
def session_management(request):
    """Session management page - view all sessions"""
    user_id = request.session.get('user_id')
    user = get_object_or_404(User, id=user_id)
    
    # Check if user has skills (can teach)
    user_skills = UserSkills.objects.filter(user=user)
    user_has_skills = user_skills.exists()
    
    # Get sessions where user is teacher (only if they have skills)
    teaching_sessions = []
    if user_has_skills:
        teaching_sessions = Session.objects.filter(teacher=user).select_related(
            'learner', 'skill', 'skill__category', 'request'
        ).order_by('-created_at')
    
    # Get sessions where user is learner
    learning_sessions = Session.objects.filter(learner=user).select_related(
        'teacher', 'skill', 'skill__category', 'request'
    ).order_by('-created_at')
    
    # Get statistics
    total_teaching = len(teaching_sessions)
    total_learning = learning_sessions.count()
    scheduled_teaching = len([s for s in teaching_sessions if s.status == 'S'])
    scheduled_learning = learning_sessions.filter(status='S').count()
    completed_teaching = len([s for s in teaching_sessions if s.status == 'C'])
    completed_learning = learning_sessions.filter(status='S').count()
    
    # Teaching Session Pagination
    teaching_paginator = Paginator(teaching_sessions, 4)
    teaching_page_number = request.GET.get("teaching_page")
    teaching_page_obj = teaching_paginator.get_page(teaching_page_number)

    # Learning Session Pagination
    learning_paginator = Paginator(learning_sessions, 4)
    learning_page_number = request.GET.get("learning_page")
    learning_page_obj = learning_paginator.get_page(learning_page_number)

    context = {
        'custom_user': user,
        'user_skills': user_skills,
        'user_has_skills': user_has_skills,
        'teaching_page_obj': teaching_page_obj,
        'learning_page_obj': learning_page_obj,
        'stats': {
            'total_teaching': total_teaching,
            'total_learning': total_learning,
            'scheduled_teaching': scheduled_teaching,
            'scheduled_learning': scheduled_learning,
            'completed_teaching': completed_teaching,
            'completed_learning': completed_learning,
        }
    }
    
    if request.headers.get("x-requested-with") == "XMLHttpRequest":
        section = request.GET.get("section")
        if section == "learning":
            html = render_to_string("category_skills/learning_sessions_grid.html", context, request=request)
        elif section == "teaching":
            html = render_to_string("category_skills/teaching_sessions_grid.html", context, request=request)
        else:
            html = ""  # fallback
        return JsonResponse({"html": html})

    return render(request, 'category_skills/sessions.html', context)


@login_required_custom
def create_session(request):
    """Create a new session from an accepted request"""
    if request.method == 'POST':
        try:
            user_id = request.session.get('user_id')
            user = get_object_or_404(User, id=user_id)
            
            request_id = request.POST.get('request_id')
            title = request.POST.get('title', '').strip()
            description = request.POST.get('description', '').strip()
            session_type = request.POST.get('session_type', 'O')
            location = request.POST.get('location', '').strip()
            scheduled_date = request.POST.get('scheduled_date')
            duration_minutes = request.POST.get('duration_minutes', 60)
            
            # Validation
            if not request_id or not title or not scheduled_date:
                return JsonResponse({'success': False, 'message': 'Required fields are missing.'})
            
            skill_request = get_object_or_404(Request, id=request_id)
            
            # Check if user is either requester or receiver of the request
            if user.id not in [skill_request.requester.id, skill_request.receiver.id]:
                return JsonResponse({'success': False, 'message': 'You are not authorized to create a session for this request.'})
            
            # Check if request is accepted
            if skill_request.status != 'A':
                return JsonResponse({'success': False, 'message': 'Only accepted requests can have sessions created.'})
            
            # Determine teacher and learner
            teacher = skill_request.receiver  # The one who has the skill
            learner = skill_request.requester  # The one who wants to learn
            
            # Create session
            new_session = Session.objects.create(
                request=skill_request,
                teacher=teacher,
                learner=learner,
                skill=skill_request.skill,
                title=title,
                description=description,
                session_type=session_type,
                location=location,
                scheduled_date=scheduled_date,
                duration_minutes=int(duration_minutes),
                status='S'  # Scheduled
            )
            
            # Create notifications for both participants
            from apps.notifications.views import create_notification
            create_notification(
                recipient=teacher,
                notification_type='session_created',
                title='Session Created',
                message=f'New session "{title}" has been created with {learner.first_name} {learner.last_name}.',
                content_object=new_session
            )
            
            create_notification(
                recipient=learner,
                notification_type='session_created',
                title='Session Created',
                message=f'New session "{title}" has been created with {teacher.first_name} {teacher.last_name}.',
                content_object=new_session
            )
            
            return JsonResponse({
                'success': True, 
                'message': 'Session created successfully!'
            })
            
        except Exception as e:
            print(f"Error in create_session: {str(e)}")
            return JsonResponse({'success': False, 'message': f'An error occurred: {str(e)}'})
    
    return JsonResponse({'success': False, 'message': 'Invalid request method.'})


@login_required_custom
def start_session(request, session_id):
    """Start a session (only teachers can start sessions)"""
    if request.method == 'POST':
        try:
            user_id = request.session.get('user_id')
            user = get_object_or_404(User, id=user_id)
            
            # Get session where user is the teacher
            session = Session.objects.filter(
                teacher=user,
                id=session_id
            ).first()
            
            if not session:
                return JsonResponse({'success': False, 'message': 'Session not found or access denied. Only teachers can start sessions.'})
            
            if session.status != 'S':
                return JsonResponse({'success': False, 'message': 'Only scheduled sessions can be started.'})
            
            # Start the session
            session.status = 'A'
            session.save()
            
            # Create notification for learner
            from apps.notifications.views import create_notification
            create_notification(
                recipient=session.learner,
                notification_type='session_started',
                title='Session Started',
                message=f'Your session "{session.title}" with {user.first_name} {user.last_name} has started!',
                content_object=session
            )
            
            return JsonResponse({
                'success': True, 
                'message': 'Session started successfully!'
            })
            
        except Exception as e:
            print(f"Error in start_session: {str(e)}")
            return JsonResponse({'success': False, 'message': f'An error occurred: {str(e)}'})
    
    return JsonResponse({'success': False, 'message': 'Invalid request method.'})

@login_required_custom
def complete_session(request, session_id):
    """Mark a session as completed (both teachers and learners can complete)"""
    if request.method == 'POST':
        try:
            user_id = request.session.get('user_id')
            user = get_object_or_404(User, id=user_id)
            
            # Get session where user is either teacher or learner
            session = Session.objects.filter(
                Q(teacher=user) | Q(learner=user),
                id=session_id
            ).first()
            
            if not session:
                return JsonResponse({'success': False, 'message': 'Session not found or access denied.'})
            
            if session.status not in ['S', 'A']:
                return JsonResponse({'success': False, 'message': 'Only scheduled or active sessions can be marked as completed.'})
            
            # Mark as completed
            session.status = 'C'
            session.completed_at = timezone.now()
            session.save()
            
            # Create notification for the other participant
            other_user = session.learner if user == session.teacher else session.teacher
            from apps.notifications.views import create_notification
            create_notification(
                recipient=other_user,
                notification_type='session_completed',
                title='Session Completed',
                message=f'Session "{session.title}" has been marked as completed by {user.first_name} {user.last_name}.',
                content_object=session
            )
            
            return JsonResponse({
                'success': True, 
                'message': 'Session marked as completed!'
            })
            
        except Exception as e:
            print(f"Error in complete_session: {str(e)}")
            return JsonResponse({'success': False, 'message': f'An error occurred: {str(e)}'})
    
    return JsonResponse({'success': False, 'message': 'Invalid request method.'})


@login_required_custom
def cancel_session(request, session_id):
    """Cancel a session"""
    if request.method == 'POST':
        try:
            user_id = request.session.get('user_id')
            user = get_object_or_404(User, id=user_id)
            
            # Get session where user is either teacher or learner
            session = Session.objects.filter(
                Q(teacher=user) | Q(learner=user),
                id=session_id
            ).first()
            
            if not session:
                return JsonResponse({'success': False, 'message': 'Session not found or access denied.'})
            
            if session.status == 'C':
                return JsonResponse({'success': False, 'message': 'Completed sessions cannot be cancelled.'})
            
            # Get cancellation reason
            reason = request.POST.get('reason', '').strip()
            if not reason:
                return JsonResponse({'success': False, 'message': 'Please provide a reason for cancellation.'})
            
            # Cancel the session
            session.status = 'CA'
            session.save()
            
            # Create notification for the other participant
            other_user = session.learner if user == session.teacher else session.teacher
            from apps.notifications.views import create_notification
            create_notification(
                recipient=other_user,
                notification_type='session_cancelled',
                title='Session Cancelled',
                message=f'Session "{session.title}" has been cancelled by {user.first_name} {user.last_name}. Reason: {reason}',
                content_object=session,
                data={'reason': reason}
            )
            
            return JsonResponse({
                'success': True, 
                'message': 'Session cancelled successfully!'
            })
            
        except Exception as e:
            print(f"Error in cancel_session: {str(e)}")
            return JsonResponse({'success': False, 'message': f'An error occurred: {str(e)}'})
    
    return JsonResponse({'success': False, 'message': 'Invalid request method.'})


@login_required_custom
def delete_session(request, session_id):
    """Delete a session"""
    if request.method == 'POST':
        try:
            user_id = request.session.get('user_id')
            user = get_object_or_404(User, id=user_id)
            
            # Get session where user is either teacher or learner
            session = Session.objects.filter(
                Q(teacher=user) | Q(learner=user),
                id=session_id
            ).first()
            
            if not session:
                return JsonResponse({'success': False, 'message': 'Session not found or access denied.'})
            
            # Delete the session
            session.delete()
            
            return JsonResponse({
                'success': True, 
                'message': 'Session deleted successfully!'
            })
            
        except Exception as e:
            print(f"Error in delete_session: {str(e)}")
            return JsonResponse({'success': False, 'message': f'An error occurred: {str(e)}'})
    
    return JsonResponse({'success': False, 'message': 'Invalid request method.'})

@login_required_custom
def leave_feedback(request, session_id):
    session = get_object_or_404(Session, id=session_id)

    if request.method == "POST":
        rating = request.POST.get("rating")
        feedback = request.POST.get("feedback", "")

        # Teacher giving feedback
        if session.teacher == request.user:
            session.teacher_rating = rating
            session.teacher_feedback = feedback

        # Learner giving feedback
        elif session.learner == request.user:
            session.learner_rating = rating
            session.learner_feedback = feedback

        else:
            return JsonResponse({"error": "Unauthorized"}, status=403)

        session.save()

        if request.headers.get("x-requested-with") == "XMLHttpRequest":
            return JsonResponse({"success": True, "message": "Feedback submitted!"})

        return redirect("category_skills:sessions")  # fallback

    return JsonResponse({"error": "Invalid request"}, status=400)