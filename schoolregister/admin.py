from django.contrib import admin
from .models import Grade, SchoolClass, SchoolYear, Semester, Student, Subject, Teacher


@admin.register(Grade)
class GradeAdmin(admin.ModelAdmin):
    list_display = ('grade', 'student', 'subject', 'semester')
    # list_display_links = ('grade', 'student', 'subject', 'semester')
    # list_editable = ('student', 'subject', 'semester')

admin.site.register(SchoolClass)

admin.site.register(SchoolYear)
# @admin.register(SchoolYear)
# class SchoolYearAdmin(admin.ModelAdmin):
    # prepopulated_fields = 

admin.site.register(Semester)

admin.site.register(Student)

admin.site.register(Subject)

admin.site.register(Teacher)
