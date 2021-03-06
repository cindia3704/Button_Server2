# Generated by Django 3.0.8 on 2020-09-08 21:00

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('button_api', '0002_auto_20200908_0414'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cloth_specific',
            name='dateBought',
            field=models.DateField(default=datetime.date(2020, 9, 9), verbose_name='date Bought'),
        ),
        migrations.AlterField(
            model_name='cloth_specific',
            name='dateLastWorn',
            field=models.DateField(default=datetime.date(2020, 9, 9), verbose_name='date Last Worn'),
        ),
    ]
