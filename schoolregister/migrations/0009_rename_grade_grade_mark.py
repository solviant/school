# Generated by Django 4.0.1 on 2022-04-19 11:32

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('schoolregister', '0008_student_user_teacher_user'),
    ]

    operations = [
        migrations.RenameField(
            model_name='grade',
            old_name='grade',
            new_name='mark',
        ),
    ]
