# Generated by Django 3.0.8 on 2020-09-04 14:13

import datetime
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import multiselectfield.db.fields


class Migration(migrations.Migration):

    dependencies = [
        ('button_api', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Cloth_Specific',
            fields=[
                ('clothID', models.AutoField(primary_key=True, serialize=False, unique=True, verbose_name='closetID')),
                ('color', models.CharField(default='NONE', max_length=64, verbose_name='cloth color')),
                ('season', multiselectfield.db.fields.MultiSelectField(choices=[('SPRING', 'Spring'), ('SUMMER', 'Summer'), ('FALL', 'Fall'), ('WINTER', 'Winter'), ('ETC', 'etc')], default='ETC', max_length=29)),
                ('category', models.CharField(choices=[('TOP', 'Top'), ('BOTTOM', 'Bottom'), ('DRESS', 'Dress'), ('OUTER', 'Outer'), ('ETC', 'etc')], default='ETC', max_length=10)),
                ('dateBought', models.DateField(default=datetime.date(2020, 9, 4), verbose_name='date Bought')),
                ('dateLastWorn', models.DateField(default=datetime.date(2020, 9, 4), verbose_name='date Last Worn')),
                ('closetID', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='User')),
            ],
        ),
    ]
