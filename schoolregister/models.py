from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
from django.urls import reverse
# z ksiazki django by example
from django.conf import settings

class Student(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, null=True, on_delete=models.SET_NULL)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    birth_date = models.DateField()
    
    # Może poprawic, zeby byla tylko linijka z return?
    @property
    def full_name(self):
        first_name = self.first_name
        last_name = self.last_name
        full_name = last_name + ' ' + first_name
        return full_name
    
    def __str__(self):
        return self.full_name
    # def __str__(self):
    #     return "{} {}".format(self.last_name, self.first_name)
    # def __str__(self):
    #     return self.last_name + ' ' + self.first_name

class SchoolYear(models.Model):
    # czy year zrobic DateField?
    start_year = models.SmallIntegerField(unique=True, validators=[MinValueValidator(2000), MaxValueValidator(2050)])
    
    @property
    ### to do: oddzielne pole - albo za pomoca @property albo przez modifikacje metody save
    def end_year(self):
        end_year = self.start_year + 1
        return end_year
    
    def __str__(self):
        return str(self.start_year) + '/' + str(self.end_year)

class Semester(models.Model):
    school_year = models.ForeignKey(SchoolYear, on_delete=models.CASCADE)
    number = models.SmallIntegerField(choices=[(1, 1), (2, 2)])
    def __str__(self):
        return str(self.school_year) + ' - ' + str(self.number)


class Subject(models.Model):
    name = models.CharField(max_length=50)
    
    def __str__(self):
        return self.name


class Teacher(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, null=True, on_delete=models.SET_NULL)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    subjects = models.ManyToManyField('Subject')
    def full_name(self):
        first_name = self.first_name
        last_name = self.last_name
        full_name = last_name + ' ' + first_name
        return full_name
    def __str__(self):
        return self.full_name() 


class SchoolClass(models.Model):
    name = models.CharField(max_length=2)
    school_year = models.ForeignKey('SchoolYear', on_delete=models.RESTRICT)
    students = models.ManyToManyField('Student')
    subjects = models.ManyToManyField('Subject')
    tutor = models.ForeignKey('Teacher', null=True, on_delete=models.SET_NULL)

    class Meta:
        verbose_name_plural = 'school classes'
    
    def year_class(self):
        year = self.school_year
        name = self.name
        year_class = str(year) + ' - ' + str(name)
        return year_class

    def __str__(self):
        return self.year_class()

    def get_absolute_url(self):
        return reverse('schoolregister:class_students', args=[self.id])


# czy dodac lub zamienic cos na school_class?
class Grade(models.Model):
    mark = models.DecimalField(max_digits=2, decimal_places=1, choices=[
        (1, 1), (1.5, 1.5), (2, 2), (2.5, 2.5), (3, 3), (3.5, 3.5), (4, 4), (4.5, 4.5), (5, 5), 
        (5.5, 5.5), (6, 6)
    ])
    school_year = models.ForeignKey('SchoolYear', on_delete=models.RESTRICT)
    semester = models.ForeignKey('Semester', on_delete=models.RESTRICT)
    subject = models.ForeignKey('Subject', on_delete=models.RESTRICT)
    student = models.ForeignKey('Student', on_delete=models.RESTRICT)
    date_added = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True)
    class GradeDescription(models.TextChoices):
        SPRAWDZIAN = 'Sprawdzian'
        KARTKOWKA = 'Kartkówka'
        ODPOWIEDZ = 'Odpowiedź'
        PRACA_DOMOWA = 'Praca domowa'
        PROJEKT = 'Projekt'
        INNE = 'Inne'
    description = models.CharField(max_length=30, choices=GradeDescription.choices)
    
    def __str__(self):
        # Mozna zmienic ze pelne liczby bez zera -> if then [:1] else return self.grade
        return str(self.mark)