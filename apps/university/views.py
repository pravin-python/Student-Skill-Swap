from django.shortcuts import render, get_object_or_404
from django.template.loader import render_to_string
from .models import University, Department, Level
from django.core.paginator import Paginator
from django.http import JsonResponse
from apps.accounts.models import User

def UniversityView(request):
    universities = University.objects.all()

    # --- Filters ---
    query = request.GET.get("q", "")
    categories = request.GET.getlist("categories[]")
    levels = request.GET.getlist("levels[]")

    if query:
        universities = universities.filter(name__icontains=query)

    if categories and "all" not in categories:
        universities = universities.filter(departments__id__in=categories).distinct()

    if levels and "all" not in levels:
        universities = universities.filter(levels__id__in=levels).distinct()

    departments = Department.objects.all()
    levels = Level.objects.all()

    paginator = Paginator(universities, 6)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    # Return JSON only when ajax=1
    if request.GET.get("ajax") == "1":
        html = render_to_string("university/university_grid.html", {
            "page_obj": page_obj,
            "section": "universities",
            "page_param": "page"
        }, request=request)
        return JsonResponse({"html": html})

    # Otherwise return full HTML page
    return render(request, 'university/university.html', {
        'departments': departments,
        'levels': levels,
        'page_obj': page_obj,
        "section": "universities",
        "page_param": "page"
    })


def UniversityDetailView(request, university_id):
    university = get_object_or_404(University, id=university_id)

    # Departments pagination
    department_qs = university.departments.all()
    dept_page_number = request.GET.get("page")
    dept_paginator = Paginator(department_qs, 4)
    dept_page_obj = dept_paginator.get_page(dept_page_number)

    # Instructors data
    instructors_data = []
    users_with_skills = User.objects.filter(
        university_name=university
    ).distinct().prefetch_related('user_skills__skill__category')

    for user in users_with_skills:
        user_skills = user.user_skills.all()
        skills_list = [us.skill for us in user_skills]
        instructors_data.append({
            "user": user,
            "skills": skills_list,
            "skills_count": len(skills_list),
        })

    # Instructors pagination
    instr_page_number = request.GET.get("instr_page")
    instr_paginator = Paginator(instructors_data, 6)  # 6 instructors per page
    instr_page_obj = instr_paginator.get_page(instr_page_number)

    # Images
    images = university.images.order_by("id")[:4]
    hero_image = images[0] if images.count() > 0 else None
    tab_side_image = images[1] if images.count() > 1 else None
    below_tab_image = images[2] if images.count() > 2 else None
    playground_image = images[3] if images.count() > 3 else None

    # Ajax partials
    if request.headers.get("x-requested-with") == "XMLHttpRequest":
        section = request.GET.get("section")
        if section == "departments":
            html = render_to_string("university/university_department.html", {
                "page_obj": dept_page_obj,
            })
            return JsonResponse({"html": html})
        elif section == "instructors":
            html = render_to_string("university/university_instructors_grid.html", {
                "instructor_page_obj": instr_page_obj,
            })
            return JsonResponse({"html": html})

    # Full page render
    context = {
        "university": university,
        "departments": university.departments.all(),
        "levels": university.levels.all(),
        "hero_image": hero_image,
        "tab_side_image": tab_side_image,
        "below_tab_image": below_tab_image,
        "playground_image": playground_image,
        "country": university.country,
        "state": university.state,
        "city": university.city,
        "page_obj": dept_page_obj,
        "instructor_page_obj": instr_page_obj,
    }
    return render(request, "university/university-details.html", context)
