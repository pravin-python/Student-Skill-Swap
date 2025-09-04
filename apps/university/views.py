from django.shortcuts import render, get_object_or_404
from django.template.loader import render_to_string
from .models import University, Department, Level
from django.core.paginator import Paginator
from django.http import JsonResponse
from apps.accounts.models import User

def UniversityView(request):
    universities = University.objects.all()

    # Filters
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

    if request.headers.get("x-requested-with") == "XMLHttpRequest":
        html = render_to_string("university/university_grid.html", {"page_obj": page_obj})
        return JsonResponse({"html": html})

    return render(request, 'university/university.html', {
        'departments': departments,
        'levels': levels,
        'page_obj': page_obj
    })


def UniversityDetailView(request, university_id):
    university = get_object_or_404(University, id=university_id)

    department_qs = university.departments.all()
    paginator = Paginator(department_qs, 4)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    images = university.images.order_by("id")[:4]
    hero_image = images[0] if images.count() > 0 else None
    tab_side_image = images[1] if images.count() > 1 else None
    below_tab_image = images[2] if images.count() > 2 else None
    playground_image = images[3] if images.count() > 3 else None

    context = {
        "university": university,
        "departments": university.departments.all(),
        "levels": university.levels.all(),
        "hero_image": hero_image,
        "tab_side_image": tab_side_image,
        "below_tab_image": below_tab_image,
        "playground_image":playground_image,
        "country": university.country,
        "state": university.state,
        "city": university.city,
        "page_obj": page_obj,
    }

    if request.headers.get("x-requested-with") == "XMLHttpRequest":
        html = render_to_string("university/university_department.html", {"page_obj": page_obj})
        return JsonResponse({"html": html})

    return render(request, "university/university-details.html", context)
