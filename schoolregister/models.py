from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
from django.urls import reverse
# z ksiazki django by example
from django.conf import settings
from django.core.exceptions import ValidationError

class Student(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, null=True, blank=True, 
    on_delete=models.SET_NULL)
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

    is_final_grade = models.BooleanField(default=False)

    @property
    def final_grade_unique_id(self):
        fg_id = self.student.id + self.subject.id + self.school_year.id + self.semester.id
        return fg_id
    
    #! Chyba trzeba tez zrobic cleana, zeby nie bylo zmiany ocen na ocene semestralna na inne sposoby?:
    """
    def clean(self)
        if not Grade.objects.annotate(num_subscribers=Count('subscriber'))
                            .filter(num_subscribers__lt=4)
                            .exists():
            raise ValidationError('The pools are all full.')
    """

    def save(self, *args, **kwargs):
        if self.is_final_grade:
            try:
                temp = Grade.objects.get(student=self.student, school_year=self.school_year,
                semester=self.semester, subject=self.subject, is_final_grade=True)
                if self != temp:
                    raise ValidationError('There can be only one final semestral grade.')
            except Grade.DoesNotExist:
                pass
        super(Grade, self).save(*args, **kwargs)

    def __str__(self):
        # Mozna zmienic ze pelne liczby bez zera -> if then [:1] else return self.grade
        return str(self.mark)

    """ Previous WIP:
    def save(self, *args, **kwargs):
        is_final_grade_in_sem = Grade.objects.filter(student=self.student, school_year=self.school_year,
        semester=self.semester, subject=self.subject)
        if not self.is_final_grade:
            super(Grade, self).save(*args, **kwargs)
        elif self.is_final_grade and is_final_grade not in all_grades_in_sem:

        if self.is_the_chosen_one:
            try:
                temp = Character.objects.get(is_the_chosen_one=True)
                if self != temp:
                    temp.is_the_chosen_one = False
                    temp.save()
            except Character.DoesNotExist:
                pass
        super(Character, self).save(*args, **kwargs)
    """

    