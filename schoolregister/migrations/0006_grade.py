# Generated by Django 4.0.1 on 2022-01-26 11:56

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('schoolregister', '0005_remove_schoolyear_end_year'),
    ]

    operations = [
        migrations.CreateModel(
            name='Grade',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('grade', models.DecimalField(choices=[(1, 1), (1.5, 1.5), (2, 2), (2.5, 2.5), (3, 3), (3.5, 3.5), (4, 4), (4.5, 4.5), (5, 5), (5.5, 5.5), (6, 6)], decimal_places=1, max_digits=2)),
                ('school_year', models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, to='schoolregister.schoolyear')),
                ('semester', models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, to='schoolregister.semester')),
                ('student', models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, to='schoolregister.student')),
                ('subject', models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, to='schoolregister.subject')),
            ],
        ),
    ]
