from django.shortcuts import render
from django.template.loader import render_to_string
from .models import University, Department, Level
from django.core.paginator import Paginator
from django.template.loader import render_to_string
from django.http import JsonResponse

def UniversityView(request):
    universities = University.objects.all()

    # Filters
    category = request.GET.get('category')
    level = request.GET.get('level')

    if category and category != "all":
        universities = universities.filter(departments__id=category)

    if level and level != "all":
        universities = universities.filter(level=level)

    departments = Department.objects.all()
    levels = Level.objects.all()

    paginator = Paginator(universities, 6)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    if request.headers.get("x-requested-with") == "XMLHttpRequest":
        html = render_to_string("university/university_grid.html", {"page_obj":page_obj})
        return JsonResponse({"html": html})
    
    return render(request, 'university/university.html', {
        'universities': universities,
        'departments': departments,
        'levels': levels,
        'page_obj' : page_obj
    })
