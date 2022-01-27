from django.http import HttpResponse
from django.shortcuts import get_object_or_404, render
from .models import Grade, SchoolYear, Semester, SchoolClass, Subject, Student, Teacher


# def test_site(request):
#     return HttpResponse("Hello, world.")


def test_site(request):
    return render(request, 'schoolregister/test_site.html')


def teacher_panel(request):
    # If logged in: nauczyciel.html; if not logged in: nauczyciel_login.html
    # Zrobic nowego managera, ktory filtruje tylko tego nauczyciela? - czy inna metoda wybierania
    # !! Czy te wszystki nizej nadal potrzebne?
    teacher = Teacher.objects.get(pk=1) # Trzeba zmienić, zeby ladowalo odpowiedniego nauczyciela
    school_years = SchoolYear.objects.all()
    semesters = Semester.objects.all()
    school_classes = SchoolClass.objects.all()
    # subjects_in_class = SchoolClass.subjects.all() # ta w shellu nie dziala: 'ManyToManyDescriptor' object has no attribute 'all'
    subjects = Subject.objects.all()
    
    return render(request, 'schoolregister/nauczyciel.html', {
        'teacher': teacher, 'school_years': school_years, 'semesters': semesters, 
        'school_classes': school_classes, 'subjects': subjects,
        })


def class_detail(request, id):
    school_class = get_object_or_404(SchoolClass, id=id)
    # subject = get_object_or_404(Subject, id=subject_id)
    students = Student.objects.all()
    grades = Grade.objects.all()
    return render(request, 'schoolregister/nauczyciel/klasa.html', {
        'school_class': school_class, 'students': students, 'grades': grades})


# def student_panel(request):
#     return render(request,)