# Generated by Django 4.0.1 on 2022-01-21 16:47

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('schoolregister', '0002_schoolclass'),
    ]

    operations = [
        migrations.AlterField(
            model_name='semester',
            name='year',
            field=models.SmallIntegerField(validators=[django.core.validators.MinValueValidator(2000), django.core.validators.MaxValueValidator(2050)]),
        ),
    ]
