from django.shortcuts import render , redirect, get_object_or_404
from django.http import JsonResponse
from django.contrib import messages
from .models import User
from django.db.models import Q
from django.contrib.auth.hashers import check_password, make_password
from .models import User, University, Department, Branch
from django.core.validators import validate_email
from django.core.exceptions import ValidationError
from apps.category_skills.models import SkillsCategory, Skills, UserSkills

def register(request):
    if request.method == "POST":
        data = request.POST
        errors = {}

        username = data.get("username", "").strip()
        first_name = data.get("first_name", "").strip()
        last_name = data.get("last_name", "").strip()
        personal_email = data.get("personal_email", "").strip()
        password = data.get("current_password", "").strip()
        confirm_password = data.get("confirm_password","").strip()
        gender = data.get("gender", "").strip()
        year = data.get("year", "").strip()
        university_id = data.get("university_name")
        department_id = data.get("department")
        branch_id = data.get("branch")

        # --- VALIDATIONS ---
        if not username:
            errors["username"] = "Username is required."
        elif User.objects.filter(username=username).exists():
            errors["username"] = "Username already exists."

        if not first_name:
            errors["first_name"] = "First name is required."
        elif not first_name.isalpha():
            errors["first_name"] = "Only Characters allowed like 'Rahul'."

        if not last_name:
            errors["last_name"] = "Last name is required."
        elif not last_name.isalpha():
            errors["last_name"] = "Only characters allowed like 'Singh'."

        if not personal_email:
            errors["personal_email"] = "Email is required."
        else:
            try:
                validate_email(personal_email)
                if User.objects.filter(personal_email=personal_email).exists():
                    errors["personal_email"] = "This email is already registered."
            except ValidationError:
                errors["personal_email"] = "Enter a valid email address."

        if not password:
            errors["current_password"] = "Password is required."
        elif len(password) < 8:
            errors["current_password"] = "Password must be at least 8 characters long."

        if not confirm_password:
            errors["confirm_password"] = "Confirm Password is required."
        elif password != confirm_password:
            errors["confirm_password"] = "Passwords do not match"
        
        valid_genders = [choice[0] for choice in User.GENDER_CHOICES]
        if not gender:
            errors["gender"] = "Gender is required."
        elif gender not in valid_genders:
            errors["gender"] = "Invalid Gender Selected"

        valid_years = [choice[0] for choice in User.YEAR_CHOICES]
        if not year:
            errors["year"] = "Year is required."
        elif year not in valid_years:
            errors["year"] = "Invalid Year Selected"

        if not university_id:
            errors["university_name"] = "Please select a university."
        elif not University.objects.filter(id=university_id).exists():
            errors["university_name"] = "Invalid university selected."

        if not department_id:
            errors["department"] = "Please select a department."
        elif not Department.objects.filter(id=department_id).exists():
            errors["department"] = "Invalid department selected."

        if not branch_id:
            errors["branch"] = "Please select a branch."
        elif not Branch.objects.filter(id=branch_id).exists():
            errors["branch"] = "Invalid branch selected."

        # --- STOP HERE IF ERRORS ---
        if errors:
            return JsonResponse({"success": False, "errors": errors})

        # --- Create user ---
        university = University.objects.get(id=university_id)
        department = Department.objects.get(id=department_id)
        branch = Branch.objects.get(id=branch_id)

        user = User(
            username=username,
            first_name=first_name,
            last_name=last_name,
            gender=gender,
            profile_pic=request.FILES.get("profile_pic"),
            university_name=university,
            personal_email=personal_email,
            department=department,
            branch=branch,
            year=year,
            bio=data.get("bio", "").strip(),
        )
        user.set_password(password)
        user.save()

        # --- Success ---
        return JsonResponse({"success": True, "message": "Registration successful! Please login."})

    return render(request, "accounts/register.html")

# View for getting the form filled with the data from backend 
def get_choices(request):
    universities = list(University.objects.values("id", "name"))
    departments = list(Department.objects.values("id", "name"))
    branches = list(Branch.objects.values("id", "name"))

    return JsonResponse({
        "universities": universities,
        "departments": departments,
        "branches": branches,
        "years": User.YEAR_CHOICES,
        "genders": User.GENDER_CHOICES,
    })

def login_view(request):
    if request.method == "POST" and request.headers.get("x-requested-with") == "XMLHttpRequest":
        username_or_email = request.POST.get("username", "").strip()
        password = request.POST.get("password", "").strip()
        errors = {}

        if not username_or_email:
            errors["username"] = "Username or Email is required."
        if not password:
            errors["password"] = "Password is required."

        if not errors:
            try:
                user = User.objects.get( Q(username=username_or_email) | Q(personal_email = username_or_email))

                if check_password(password, user.current_password):
                    request.session["user_id"] = user.id
                    return JsonResponse({"success": True})
                else:
                    errors["password"] = "Invalid Username or Password."
            except User.DoesNotExist:
                errors["username"] = "Invalid Username or Password"

        return JsonResponse({"success": False, "errors": errors})

    return redirect("core:home")

def logout_view(request):
    # Clear only your custom session keys
    request.session.flush()  # clears entire session safely
    messages.success(request, "You have been logged out successfully.")
    return redirect("core:home")

def login_required_custom(view_func):
    """Custom decorator to check if user is logged in"""
    def wrapper(request, *args, **kwargs):
        if 'user_id' not in request.session:
            messages.error(request, "Please log in to access this page.")
            return redirect("core:home")
        return view_func(request, *args, **kwargs)
    return wrapper

@login_required_custom
def dashboard(request):
    """Dashboard view showing user's overview and stats"""
    user_id = request.session.get('user_id')
    user = get_object_or_404(User, id=user_id)
    
    # Get skill categories for display
    skill_categories = SkillsCategory.objects.all()[:6]  # Limit to 6 for display
    
    # Get some recommended skills (you can implement more sophisticated logic later)
    recommended_skills = Skills.objects.all()[:3]
    
    context = {
        'custom_user': user,
        'skill_categories': skill_categories,
        'recommended_skills': recommended_skills,
        'enrolled_skills_count': 0,  # Placeholder - implement when enrollment system is ready
        'completed_courses_count': 0,  # Placeholder - implement when completion tracking is ready
    }
    
    return render(request, 'accounts/dashboard.html', context)

@login_required_custom
def profile(request):
    """Profile view showing user's complete information"""
    user_id = request.session.get('user_id')
    user = get_object_or_404(User, id=user_id)
    
    # Get choices for dropdowns
    universities = University.objects.all()
    departments = Department.objects.all()
    branches = Branch.objects.all()
    
    # Get user's skills
    user_skills = UserSkills.objects.filter(user=user).select_related('skill__category')
    user_skill_ids = [us.skill.id for us in user_skills]
    
    # Get available skills (skills not added by user)
    available_skills = Skills.objects.exclude(id__in=user_skill_ids).select_related('category')
    
    context = {
        'custom_user': user,
        'universities': universities,
        'departments': departments,
        'branches': branches,
        'gender_choices': User.GENDER_CHOICES,
        'year_choices': User.YEAR_CHOICES,
        'user_skills': user_skills,
        'available_skills': available_skills,
    }
    
    return render(request, 'accounts/profile.html', context)

@login_required_custom
def update_profile(request):
    """Update user profile information"""
    if request.method == "POST" and request.headers.get("x-requested-with") == "XMLHttpRequest":
        user_id = request.session.get('user_id')
        user = get_object_or_404(User, id=user_id)
        
        data = request.POST
        errors = {}
        
        # Get form data
        first_name = data.get("first_name", "").strip()
        last_name = data.get("last_name", "").strip()
        personal_email = data.get("personal_email", "").strip()
        gender = data.get("gender", "").strip()
        year = data.get("year", "").strip()
        university_id = data.get("university_name")
        department_id = data.get("department")
        branch_id = data.get("branch")
        bio = data.get("bio", "").strip()
        
        # Validations
        if not first_name:
            errors["first_name"] = "First name is required."
        if not last_name:
            errors["last_name"] = "Last name is required."
            
        if not personal_email:
            errors["personal_email"] = "Email is required."
        else:
            try:
                validate_email(personal_email)
                # Check if email is already taken by another user
                existing_user = User.objects.filter(personal_email=personal_email).exclude(id=user.id).first()
                if existing_user:
                    errors["personal_email"] = "This email is already registered."
            except ValidationError:
                errors["personal_email"] = "Enter a valid email address."
        
        if not gender:
            errors["gender"] = "Gender is required."
        if not year:
            errors["year"] = "Year is required."
            
        if not university_id:
            errors["university_name"] = "Please select a university."
        elif not University.objects.filter(id=university_id).exists():
            errors["university_name"] = "Invalid university selected."
            
        if not department_id:
            errors["department"] = "Please select a department."
        elif not Department.objects.filter(id=department_id).exists():
            errors["department"] = "Invalid department selected."
            
        if not branch_id:
            errors["branch"] = "Please select a branch."
        elif not Branch.objects.filter(id=branch_id).exists():
            errors["branch"] = "Invalid branch selected."
            
        if len(bio) > 250:
            errors["bio"] = "Bio must be less than 250 characters."
        
        # Stop here if errors
        if errors:
            return JsonResponse({"success": False, "errors": errors})
        
        # Update user
        try:
            university = University.objects.get(id=university_id)
            department = Department.objects.get(id=department_id)
            branch = Branch.objects.get(id=branch_id)
            
            user.first_name = first_name
            user.last_name = last_name
            user.personal_email = personal_email
            user.gender = gender
            user.year = year
            user.university_name = university
            user.department = department
            user.branch = branch
            user.bio = bio
            
            # Handle profile picture if uploaded
            if 'profile_pic' in request.FILES:
                user.profile_pic = request.FILES['profile_pic']
            
            user.save()
            
            return JsonResponse({"success": True, "message": "Profile updated successfully!"})
            
        except Exception as e:
            return JsonResponse({"success": False, "errors": {"general": "An error occurred while updating your profile."}})
    
    return JsonResponse({"success": False, "errors": {"general": "Invalid request."}})

@login_required_custom
def change_password(request):
    """Change user password with previous password storage"""
    if request.method == "POST" and request.headers.get("x-requested-with") == "XMLHttpRequest":
        user_id = request.session.get('user_id')
        user = get_object_or_404(User, id=user_id)
        
        data = request.POST
        errors = {}
        
        current_password = data.get("current_password", "").strip()
        new_password = data.get("new_password", "").strip()
        confirm_password = data.get("confirm_password", "").strip()
        
        # --- Validations ---
        if not current_password:
            errors["current_password"] = "Current password is required."
        elif not check_password(current_password, user.current_password):
            errors["current_password"] = "Current password is incorrect."
            
        if not new_password:
            errors["new_password"] = "New password is required."
        elif len(new_password) < 8:
            errors["new_password"] = "New password must be at least 8 characters long."
        elif check_password(new_password, user.current_password):
            errors["new_password"] = "New password must be different from current password."
            
        if not confirm_password:
            errors["confirm_password"] = "Please confirm your new password."
        elif new_password != confirm_password:
            errors["confirm_password"] = "Passwords do not match."
        
        # Stop here if errors
        if errors:
            return JsonResponse({"success": False, "errors": errors})
        
        try:
            # Save previous hashed password
            user.previous_password = user.current_password
            
            # Save new hashed password
            user.current_password = make_password(new_password)
            user.save()
            
            return JsonResponse({"success": True, "message": "Password changed successfully!"})
            
        except Exception:
            return JsonResponse({"success": False, "errors": {"general": "An error occurred while changing your password."}})
    
    return JsonResponse({"success": False, "errors": {"general": "Invalid request"}})