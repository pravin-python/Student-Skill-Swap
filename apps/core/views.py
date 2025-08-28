from django.shortcuts import render
from django.db.models import Count
from apps.category_skills.models import SkillsCategory

def HomeView(request):
    categories = SkillsCategory.objects.annotate(course_count = Count("skills"))
    return render (request , "core/index.html" , {"categories" : categories})

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