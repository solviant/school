from django import forms
from django.contrib.auth.models import User
from .models import Grade, Subject




class GradeForm(forms.ModelForm):

    subject = forms.ModelChoiceField(queryset=Subject.objects.all(), widget=forms.HiddenInput())

    class Meta:
        model = Grade
        fields = ('grade', 'school_year', 'semester', 'subject', 'student',)

    # class GradeFormAuto()
    # widget = forms.HiddenInput()

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
