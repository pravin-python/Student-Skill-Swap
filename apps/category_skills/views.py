from django.shortcuts import render
from .models import SkillsCategory, Skills
from django.core.paginator import Paginator
from django.http import JsonResponse
from django.template.loader import render_to_string

from django.template.loader import render_to_string

def CourseView(request):
    categories = SkillsCategory.objects.all()
    skills_qs = Skills.objects.select_related("category").all()

    # Search filter
    search_query = request.GET.get("q")
    if search_query:
        skills_qs = skills_qs.filter(name__icontains=search_query)

    # Category filter
    category_ids = request.GET.getlist("categories[]")  # expects categories[]=1&categories[]=2
    if category_ids and "all" not in category_ids:
        skills_qs = skills_qs.filter(category_id__in=category_ids)

    paginator = Paginator(skills_qs, 6)
    page_number = request.GET.get("page")
    skills = paginator.get_page(page_number)

    if request.headers.get("x-requested-with") == "XMLHttpRequest":
        html = render_to_string("category_skills/courses_grid.html", {"skills": skills})
        return JsonResponse({"html": html})

    return render(
        request,
        "category_skills/courses.html",
        {"categories": categories, "skills": skills},
    )



def CourseDetailView(request):
    return render(request, "category_skills/course-details.html")

def InstructorView(request):
    return render(request, "category_skills/instructors.html")
