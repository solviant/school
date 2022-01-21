from tkinter import CASCADE
from django.db import models

class Student(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    birth_date = models.DateField()

class Semester(models.Model):
    year = models.SmallIntegerField()
    number = models.SmallIntegerField(choices=[(1, 1), (2, 2)])

class Subject(models.Model):
    name = models.CharField(max_length=50)

class Teacher(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    subjects = models.ManyToManyField('Subject')

class SchoolClass:
    name = models.CharField(max_length=2)
    semester = models.ForeignKey('Semester', on_delete=models.CASCADE)
    students = models.ManyToManyField('Student')
    subjects = models.ManyToManyField('Subject')
    tutor = models.ForeignKey('Teacher', on_delete=models.RESTRICT)
