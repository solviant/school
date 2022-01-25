from tabnanny import verbose
from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator

class Student(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    birth_date = models.DateField()
    #! sprawdzic czy ta def dziala??
    def full_name(self):
        first_name = self.first_name
        last_name = self.last_name
        full_name = last_name + ' ' + first_name
        return full_name
    def __str__(self):
        return self.full_name()
    # def __str__(self):
    #     return "{} {}".format(self.last_name, self.first_name)
    # def __str__(self):
    #     return self.last_name + ' ' + self.first_name

class SchoolYear(models.Model):
    # czy year zrobic DateField?
    start_year = models.SmallIntegerField(unique=True, validators=[MinValueValidator(2000), MaxValueValidator(2050)])
    end_year = models.SmallIntegerField(unique=True, validators=[MinValueValidator(2000), MaxValueValidator(2050)])
    # def end_year(self):
    #     end_year = self.start_year + 1
    #     return end_year
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
    tutor = models.ForeignKey('Teacher', on_delete=models.SET_NULL)

    class Meta:
        verbose_name_plural = 'school classes'
    
    def class_semester(self):
        name = self.name
        semester = self.semester
        class_semester = name + ' ' + semester
        return class_semester

    def __str__(self):
        return self.class_semester
