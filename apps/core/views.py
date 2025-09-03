from django.shortcuts import render
from django.db.models import Count
from apps.accounts.models import User
from apps.category_skills.models import SkillsCategory , Skills
from django.template.loader import render_to_string
from django.core.paginator import Paginator
from django.http import JsonResponse

def HomeView(request):
    categories = SkillsCategory.objects.all()
    
    # Get all skills that have been added by users
    skills_qs = Skills.objects.select_related("category").filter(user_skills__isnull=False).distinct()


    # Exclude skills added by the current user if logged in
    if 'user_id' in request.session:
        user_id = request.session.get('user_id')
        skills_qs = skills_qs.exclude(user_skills__user_id=user_id)

    skills = skills_qs.order_by("?")[:6]

    if request.headers.get("x-requested-with") == "XMLHttpRequest":
        html = render_to_string("core/index.html", {"skills": skills})
        return JsonResponse({"html": html})

    # Get all users who have added skills
    users_with_skills = User.objects.filter(user_skills__isnull=False).distinct().prefetch_related('user_skills__skill__category')
    
    # Group skills by user
    instructors_data = []
    for user in users_with_skills:
        user_skills = user.user_skills.all()
        skills_list = [us.skill for us in user_skills]
        instructors_data.append({
            'user': user,
            'skills': skills_list,
            'skills_count': len(skills_list)
        })

    return render(
        request,
        "core/index.html",
        {"categories": categories, "skills": skills , "level_choices" : Skills.LEVEL_CHOICES , "instructors_data" : instructors_data},
    )

 
def AboutView(request):
    return render (request , "core/about.html")

def ContactView(request):
    return render(request , "core/contact.html")

def TermsView(request):
    return render(request , "core/terms.html")

def PrivacyView(request):
    return render(request , "core/privacy.html")

def EnrollView(request):
    return render(request , "core/enroll.html")