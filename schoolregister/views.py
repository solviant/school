from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, render
from .forms import LoginForm, UserRegistrationForm
from .models import Grade, SchoolYear, Semester, SchoolClass, Subject, Student, Teacher


# def test_site(request):
#     return HttpResponse("Hello, world.")


def test_site(request):
    return render(request, 'schoolregister/test_site.html')


def user_login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            user = authenticate(request, username=cd['username'], password=cd['password'])
            if user is not None:
                if user.is_active:
                    login(request, user)
                    return HttpResponse('Authenticated successfully')
                else:
                    return HttpResponse('Disabled account')
            else:
                return HttpResponse('Invalid login')
    else:
            form = LoginForm()
    return render(request, 'schoolregister/login.html', {'form': form})



def teacher_panel(request):
    # If logged in: nauczyciel.html; if not logged in: nauczyciel_login.html
    # Zrobic nowego managera, ktory filtruje tylko tego nauczyciela? - czy inna metoda wybierania
    # !! Czy te wszystki nizej nadal potrzebne?
    teacher = Teacher.objects.get(pk=1) # !!Trzeba zmienić, zeby ladowalo odpowiedniego nauczyciela
    school_years = SchoolYear.objects.all()
    semesters = Semester.objects.all()
    school_classes = SchoolClass.objects.all()
    # subjects_in_class = SchoolClass.subjects.all() # !!ta w shellu nie dziala: 'ManyToManyDescriptor' object has no attribute 'all'
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
    subject = Subject.objects.get(pk=1) # !! To jest do zmiany, na razie wpisane na twardo jako test - przyklad.
    return render(request, 'schoolregister/nauczyciel/klasa.html', {
        'school_class': school_class, 'students': students, 'grades': grades, 'subject': subject})


@login_required
def dashboard(request):
    return render(request, 'schoolregister/dashboard.html', {'section': 'dashboard'})


# def student_panel(request):
#     return render(request,)

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