from django.shortcuts import render

def CourseView(request):
    return render(request , "category_skills/courses.html")

def CourseDetailView(request):
    return render(request , "category_skills/course-details.html")

def InstructorView(request):
    return render(request , "category_skills/instructors.html")