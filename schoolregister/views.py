from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, render
from .forms import LoginForm, UserRegistrationForm, GradeForm
from .models import Grade, SchoolYear, Semester, SchoolClass, Subject, Student, Teacher


"""Poprzednia wersja logowania"""
# def user_login(request):
#     if request.method == 'POST':
#         form = LoginForm(request.POST)
#         if form.is_valid():
#             cd = form.cleaned_data
#             user = authenticate(request, username=cd['username'], password=cd['password'])
#             if user is not None:
#                 if user.is_active:
#                     login(request, user)
#                     return HttpResponse('Authenticated successfully')
#                 else:
#                     return HttpResponse('Disabled account')
#             else:
#                 return HttpResponse('Invalid login')
#     else:
#             form = LoginForm()
#     return render(request, 'schoolregister/login.html', {'form': form})


@login_required
def teacher_panel(request):
    # If logged in: nauczyciel.html; if not logged in: nauczyciel_login.html
    # Zrobic nowego managera, ktory filtruje tylko tego nauczyciela? - czy inna metoda wybierania - podobnie jak: django3byexample.pdf p. 25
    # !! Czy te wszystki nizej nadal potrzebne?
    teacher = Teacher.objects.get(user=request.user) # !!Trzeba zmienić, zeby ladowalo odpowiedniego nauczyciela
    school_years = SchoolYear.objects.all()
    semesters = Semester.objects.all()
    school_classes = SchoolClass.objects.all()
    # subjects_in_class = SchoolClass.subjects.all() # !!ta w shellu nie dziala: 'ManyToManyDescriptor' object has no attribute 'all'
    subjects = Subject.objects.all()
    
    return render(request, 'schoolregister/nauczyciel.html', {
        'teacher': teacher, 'school_years': school_years, 'semesters': semesters, 
        'school_classes': school_classes, 'subjects': subjects,
        })


# !! Proba zeby zadzialalo:
@login_required
def class_students(request, school_class_id):
    school_class = get_object_or_404(SchoolClass, id=school_class_id)
    # subject = get_object_or_404(Subject, id=subject_id)
    students = Student.objects.all()
    return render(request, 'schoolregister/nauczyciel/klasa_uczniowie.html', {
        'school_class': school_class, 'students': students})


# !! Trzeba sprawdzic, czy zwykly uczen po wpisaniu adresu moze sie dostac.
@login_required
def class_detail(request, school_class_id, subject_id):
    school_class = get_object_or_404(SchoolClass, id=school_class_id)
    # subject = get_object_or_404(Subject, id=subject_id)
    students = Student.objects.all()
    grades = Grade.objects.all()
    subject = get_object_or_404(Subject, id=subject_id) # !! <Subject.objects.get(pk=1)> To jest do zmiany, na razie wpisane na twardo jako test - przyklad.
    return render(request, 'schoolregister/nauczyciel/klasa.html', {
        'school_class': school_class, 'students': students, 'grades': grades, 'subject': subject})


@login_required
def dashboard(request):
    return render(request, 'schoolregister/dashboard.html', {'section': 'dashboard'})


def register(request):
    if request.method == 'POST':
        user_form = UserRegistrationForm(request.POST)
        if user_form.is_valid():
            # Create a new user object but avoid saving it yet
            new_user = user_form.save(commit=False)
            # Set the chosen password
            new_user.set_password(
                user_form.cleaned_data['password'])
            # Save the user object
            new_user.save()
            return render(request,
            'schoolregister/register_done.html',
            {'new_user': new_user})
    else:
        user_form = UserRegistrationForm()
    return render(request, 'schoolregister/register.html',
    {'user_form': user_form})



# def test_site(request):
#     return HttpResponse("Hello, world.")


def test_site(request):
    return render(request, 'schoolregister/test_site.html')


def test_site02(request):
    grade_form = GradeForm()
    return render(request, 'schoolregister/test_site02.html',
    {'grade_form': grade_form})