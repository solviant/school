from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
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
    semesters = school_class.school_year.semester_set.all()
    students = Student.objects.all() # czy tu <class>_set.all po school_class?
    students_list = []
    grades = Grade.objects.all() # czy tu <class>_set.all po school_class?
    subject = Subject.objects.get(id=subject_id) # !! <Subject.objects.get(pk=1)> To jest do zmiany, na razie wpisane na twardo jako test - przyklad.
    grades_list_1st = []
    grades_list_2nd = []
    uczniowie_lista = []
    grades_list = []
    # students_grades = [{'students': uczniowie_lista}, {'grades': []}]
    x = {'Wozniak': [1, 2, 3]}
    max_count_grades_1st = 0
    max_count_grades_2nd = 0
    semesters_len = len(semesters)
    i = -1

    # for sc_student in school_class.students.all():
    #     students_list.append(sc_student)
    #     grades_list.append(sc_student.grade_set.filter(school_year_id=school_class.school_year.id, semester_id=1, subject_id=1, student_id=sc_student.id))
    # students_grades = zip(students_list, grades_list)
    # [[students], [[scs_grades],[],...]]

    if request.method == 'POST':
        grade_form = GradeForm(request.POST)
        # grade_form.subject = subject  # To nie działa
        if grade_form.is_valid():
            grade_form.save()
            return HttpResponseRedirect('')
        # else:
        #     return HttpResponse("Error.")
    else:
        grade_form = GradeForm()
        # grade_form.subject = subject  # To nie działa


    # w petli najpierw powinien byc semester

    for sc_student in school_class.students.all():
        students_list.append(sc_student)
        grades_list.append(sc_student.grade_set.filter(school_year_id=school_class.school_year.id, semester_id=1, subject_id=1, student_id=sc_student.id))
        # sprawdzic mozliwosc uzycia "entry_set"
        for semester in semesters:
            if semester.number == 1:
                grades_count_1st = len(grades.filter(school_year_id=school_class.school_year.id, semester_id=semester.id, subject_id=subject.id, student_id=sc_student.id))
                if max_count_grades_1st < grades_count_1st:
                    max_count_grades_1st = grades_count_1st
                
                
                
    for sc_student in school_class.students.all():
        for semester in semesters:
            if semester.number == 1:            
                for grade in grades:
                    if grade.student == sc_student and grade.subject == subject and grade.semester == semester:
                        grades_list_1st.append(grade)
                        # if student_grades[sc_student.full_name]:
                        # i += 1
                        # uczniowie_lista.append(sc_student)
            elif semester.number == 2:
                grades_count_2nd = len(grades.filter(school_year_id=school_class.school_year.id, semester_id=semester.id, subject_id=subject.id, student_id=sc_student.id))
                if max_count_grades_2nd < grades_count_2nd:
                    max_count_grades_2nd = grades_count_2nd
                for grade in grades:
                    if grade.student == sc_student and grade.subject == subject and grade.semester == semester:
                        grades_list_2nd.append(grade)
                        max_count_grades_2nd += 1
    
    col_span_1_sem = max_count_grades_1st + 3
    col_span_2_sem = max_count_grades_2nd + 3
    col_span_year = col_span_1_sem + col_span_2_sem

    return render(request, 'schoolregister/nauczyciel/klasa.html', {
        'school_class': school_class, 'students': students, 
        'grades': grades, 'subject': subject, 'grade_form': grade_form,
        'students_list': students_list,
        'grades_list': grades_list,
        'grades_list_1st': grades_list_1st,
        'grades_list_2nd': grades_list_2nd,
        'max_count_grades_1st': max_count_grades_1st,
        'max_count_grades_2nd': max_count_grades_2nd, 
        'col_span_1_sem': col_span_1_sem,
        'col_span_2_sem': col_span_2_sem,
        'col_span_year': col_span_year,
        'semesters': semesters,
        'semesters_len': semesters_len,})


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
    if request.method == 'POST':
        grade_form = GradeForm(request.POST)
        if grade_form.is_valid():
            grade_form.save()
            return HttpResponseRedirect('')
        else:
            return HttpResponse("Error.")

    else:
        grade_form = GradeForm()

    return render(request, 'schoolregister/test_site02.html',
    {'grade_form': grade_form})


def test_site03(request):
    return render(request, 'schoolregister/test_site03.html')

def test_site04(request):
    return render(request, 'schoolregister/test_site04.html')