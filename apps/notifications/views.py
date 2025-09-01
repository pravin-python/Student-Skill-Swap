from django.shortcuts import render
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_http_methods
from django.utils import timezone
from .models import Notification
from apps.accounts.views import login_required_custom

@login_required_custom
def get_notifications(request):
    """Get user's notifications"""
    try:
        user_id = request.session.get('user_id')
        if not user_id:
            return JsonResponse({'success': False, 'message': 'User not logged in'})
        
        # Get unread notifications count
        unread_count = Notification.objects.filter(
            recipient_id=user_id, 
            is_read=False
        ).count()
        
        # Get recent notifications (last 20)
        notifications = Notification.objects.filter(
            recipient_id=user_id
        ).order_by('-created_at')[:20]
        
        notifications_data = []
        for notification in notifications:
            notifications_data.append({
                'id': notification.id,
                'title': notification.title,
                'message': notification.message,
                'notification_type': notification.notification_type,
                'is_read': notification.is_read,
                'created_at': notification.created_at.strftime('%M minutes ago') if notification.is_recent else notification.created_at.strftime('%b %d, %Y'),
                'is_recent': notification.is_recent,
            })
        
        return JsonResponse({
            'success': True,
            'unread_count': unread_count,
            'notifications': notifications_data
        })
        
    except Exception as e:
        print(f"Error in get_notifications: {str(e)}")
        return JsonResponse({'success': False, 'message': 'Error fetching notifications'})

@login_required_custom
@require_http_methods(["POST"])
def mark_as_read(request, notification_id):
    """Mark a specific notification as read"""
    try:
        user_id = request.session.get('user_id')
        if not user_id:
            return JsonResponse({'success': False, 'message': 'User not logged in'})
        
        notification = Notification.objects.filter(
            id=notification_id,
            recipient_id=user_id
        ).first()
        
        if not notification:
            return JsonResponse({'success': False, 'message': 'Notification not found'})
        
        notification.is_read = True
        notification.save()
        
        return JsonResponse({'success': True, 'message': 'Notification marked as read'})
        
    except Exception as e:
        print(f"Error in mark_as_read: {str(e)}")
        return JsonResponse({'success': False, 'message': 'Error marking notification as read'})

@login_required_custom
@require_http_methods(["POST"])
def mark_all_as_read(request):
    """Mark all user's notifications as read"""
    try:
        user_id = request.session.get('user_id')
        if not user_id:
            return JsonResponse({'success': False, 'message': 'User not logged in'})
        
        Notification.objects.filter(
            recipient_id=user_id,
            is_read=False
        ).update(is_read=True)
        
        return JsonResponse({'success': True, 'message': 'All notifications marked as read'})
        
    except Exception as e:
        print(f"Error in mark_all_as_read: {str(e)}")
        return JsonResponse({'success': False, 'message': 'Error marking notifications as read'})

def create_notification(recipient, notification_type, title, message, content_object=None, data=None):
    """Utility function to create notifications"""
    try:
        notification = Notification.objects.create(
            recipient=recipient,
            notification_type=notification_type,
            title=title,
            message=message,
            content_object=content_object,
            data=data or {}
        )
        return notification
    except Exception as e:
        print(f"Error creating notification: {str(e)}")
        return None
