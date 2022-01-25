from django.contrib import admin
from .models import SchoolClass, Semester, Student, Subject, Teacher

admin.site.register(SchoolClass)
admin.site.register(Semester)
admin.site.register(Student)
admin.site.register(Subject)
admin.site.register(Teacher)
