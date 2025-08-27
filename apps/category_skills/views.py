from django.shortcuts import render
from .models import Skills, SkillsCategory
from django.db.models import Q

def CourseView(request):
    skills = Skills.objects.all()
    categories = SkillsCategory.objects.all()

    # --- Search ---
    search_query = request.GET.get("search", "").strip()
    if search_query:
        skills = skills.filter(
            Q(name__icontains=search_query) | Q(description__icontains=search_query)
        )

    # --- Filter by category ---
    category_id = request.GET.get("category")
    if category_id and category_id != "All":
        skills = skills.filter(category__id=category_id)

    context = {
        "skills": skills,
        "categories": categories,
        "search_query": search_query,
        "selected_category": category_id,
    }
    return render(request, "category_skills/courses.html", context)


def CourseDetailView(request):
    return render(request , "category_skills/course-details.html")

def InstructorView(request):
    return render(request , "category_skills/instructors.html")