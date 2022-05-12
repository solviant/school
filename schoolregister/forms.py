from django import forms
from django.contrib.auth.models import User
from .models import Grade, SchoolYear, Semester, Subject, Student




class GradeForm(forms.ModelForm):
    school_year = forms.ModelChoiceField(queryset=SchoolYear.objects.all(), widget=forms.HiddenInput())
    semester = forms.ModelChoiceField(queryset=Semester.objects.all(), widget=forms.HiddenInput())
    subject = forms.ModelChoiceField(queryset=Subject.objects.all(), widget=forms.HiddenInput())
    student = forms.ModelChoiceField(queryset=Student.objects.all(), widget=forms.HiddenInput())
    
    class Meta:
        model = Grade
        fields = ('mark', 'school_year', 'semester', 'subject', 'student', 'description')

    # class GradeFormAuto()
    # widget = forms.HiddenInput()


class GradeToEdit(forms.ModelForm):
    class Meta:
        model = Grade
        fields = ('mark', 'school_year', 'semester', 'subject', 'student', 
        'description', 'is_final_grade')


class FinalGradeForm(forms.ModelForm):
    school_year = forms.ModelChoiceField(queryset=SchoolYear.objects.all(), widget=forms.HiddenInput())
    semester = forms.ModelChoiceField(queryset=Semester.objects.all(), widget=forms.HiddenInput())
    subject = forms.ModelChoiceField(queryset=Subject.objects.all(), widget=forms.HiddenInput())
    student = forms.ModelChoiceField(queryset=Student.objects.all(), widget=forms.HiddenInput())
    is_final_grade = forms.BooleanField(widget=forms.HiddenInput())
    
    class Meta:
        model = Grade
        fields = ('mark', 'school_year', 'semester', 'subject', 'student', 
        'description', 'is_final_grade')


class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)


class UserRegistrationForm(forms.ModelForm):
    password = forms.CharField(label='Password',
    widget=forms.PasswordInput)
    password2 = forms.CharField(label='Repeat password',
    widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ('username', 'first_name', 'email')

    def clean_password2(self):
        cd = self.cleaned_data
        if cd['password'] != cd['password2']:
            raise forms.ValidationError('Passwords don\'t match.')
        return cd['password2']
