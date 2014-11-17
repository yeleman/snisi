# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('snisi_core', '0003_auto_20141117_1551'),
        ('snisi_epidemiology', '0002_auto_20141008_1439'),
    ]

    operations = [
        migrations.CreateModel(
            name='EpidemiologyAlertR',
            fields=[
                ('snisireport_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='snisi_core.SNISIReport')),
                ('disease', models.SlugField(verbose_name='Disease', choices=[('red_diarrhea', 'Red Diarrhea'), ('neonatal_tetanus', 'NNT'), ('meningitis', 'Meningitis'), ('rabies', 'Rabies'), ('cholera', 'Cholera'), ('acute_measles_diarrhea', 'Acute Measles Diarrhea'), ('other_notifiable_disease', 'Other Notifiable Diseases'), ('yellow_fever', 'Yellow Fever'), ('influenza_a_h1n1', 'Influenza A H1N1'), ('acute_flaccid_paralysis', 'AFP'), ('ebola', 'Ebola'), ('measles', 'Measles')])),
                ('suspected_cases', models.PositiveIntegerField(verbose_name='Suspected cases')),
                ('confirmed_cases', models.PositiveIntegerField(verbose_name='Confirmed cases')),
                ('deaths', models.PositiveIntegerField(verbose_name='Deaths')),
                ('date', models.DateField()),
            ],
            options={
                'verbose_name': 'Epidemiology Alert',
                'verbose_name_plural': 'Epidemiology Alerts',
            },
            bases=('snisi_core.snisireport',),
        ),
    ]
