# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('snisi_core', '0010_auto_20150710_1405'),
    ]

    operations = [
        migrations.CreateModel(
            name='CATMissionR',
            fields=[
                ('snisireport_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='snisi_core.SNISIReport')),
                ('started_on', models.DateField(verbose_name='Start Date')),
                ('ended_on', models.DateField(null=True, verbose_name='End Date', blank=True)),
                ('operator_type', models.CharField(max_length=75, verbose_name='Operatr Profile', choices=[('OPT', 'OPT'), ('TSO', 'TSO'), ('AMO', 'AMO')])),
                ('strategy', models.CharField(max_length=75, verbose_name='Strategy', choices=[('mobile', 'Mobile'), ('fixed', 'Fixed'), ('advanced', 'Advanced')])),
                ('nb_surgery_male', models.PositiveIntegerField(default=0)),
                ('nb_surgery_female', models.PositiveIntegerField(default=0)),
                ('nb_surgery_right_eye', models.PositiveIntegerField(default=0)),
                ('nb_surgery_left_eye', models.PositiveIntegerField(default=0)),
                ('nb_age_under_15', models.PositiveIntegerField(default=0)),
                ('nb_age_under_18', models.PositiveIntegerField(default=0)),
                ('nb_age_under_20', models.PositiveIntegerField(default=0)),
                ('nb_age_under_25', models.PositiveIntegerField(default=0)),
                ('nb_age_under_30', models.PositiveIntegerField(default=0)),
                ('nb_age_under_35', models.PositiveIntegerField(default=0)),
                ('nb_age_under_40', models.PositiveIntegerField(default=0)),
                ('nb_age_under_45', models.PositiveIntegerField(default=0)),
                ('nb_age_under_50', models.PositiveIntegerField(default=0)),
                ('nb_age_over_50', models.PositiveIntegerField(default=0)),
                ('nb_surgery_reports', models.PositiveIntegerField(default=0, verbose_name='Nb of surgeries')),
                ('nb_days_min', models.PositiveIntegerField(default=0)),
                ('nb_days_max', models.PositiveIntegerField(default=0)),
                ('nb_days_mean', models.FloatField(default=0)),
                ('nb_days_median', models.FloatField(default=0)),
                ('nb_days_total', models.PositiveIntegerField(default=0)),
                ('operator', models.ForeignKey(verbose_name='Operator', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'CAT Surgery Mission Report',
                'verbose_name_plural': 'CAT Surgery Mission Reports',
            },
            bases=('snisi_core.snisireport',),
        ),
        migrations.CreateModel(
            name='CATSurgeryR',
            fields=[
                ('snisireport_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='snisi_core.SNISIReport')),
                ('surgery_ident', models.CharField(max_length=5)),
                ('surgery_date', models.DateField()),
                ('gender', models.CharField(max_length=20, choices=[('right', 'R.E'), ('left', 'L.E')])),
                ('eye', models.CharField(max_length=20, choices=[('right', 'R.E'), ('left', 'L.E')])),
                ('age', models.PositiveIntegerField(help_text='in years')),
                ('result_date', models.DateField(null=True, blank=True)),
                ('visual_acuity', models.PositiveIntegerField(null=True, blank=True)),
                ('location', models.ForeignKey(to='snisi_core.Entity')),
            ],
            options={
                'verbose_name': 'CAT Surgery Report',
                'verbose_name_plural': 'CAT Surgery Reports',
            },
            bases=('snisi_core.snisireport',),
        ),
        migrations.AddField(
            model_name='catmissionr',
            name='surgery_reports',
            field=models.ManyToManyField(to='snisi_cataract.CATSurgeryR', verbose_name='Surgery Reports', blank=True),
        ),
    ]
