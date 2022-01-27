from django.http import HttpResponse
from django.shortcuts import render
from .models import SchoolYear, Semester, Subject, Student, Grade


# def test_site(request):
#     return HttpResponse("Hello, world.")

def test_site(request):
    return render(request, 'schoolregister/test_site.html')


# def teacher_panel(request):
#     school_year = 

# def student_panel(request):
#     return render(request,)