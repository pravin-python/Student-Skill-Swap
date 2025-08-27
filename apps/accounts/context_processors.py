from .models import User

def custom_user(request):
    user_obj = None
    if request.session.get("user_id"):
        try:
            user_obj = User.objects.get(id=request.session["user_id"])
        except User.DoesNotExist:
            pass
    return {"custom_user": user_obj}