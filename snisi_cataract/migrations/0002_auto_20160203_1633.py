# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('snisi_cataract', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='catmissionr',
            name='nb_days_max',
        ),
        migrations.RemoveField(
            model_name='catmissionr',
            name='nb_days_mean',
        ),
        migrations.RemoveField(
            model_name='catmissionr',
            name='nb_days_median',
        ),
        migrations.RemoveField(
            model_name='catmissionr',
            name='nb_days_min',
        ),
        migrations.RemoveField(
            model_name='catmissionr',
            name='nb_days_total',
        ),
        migrations.AddField(
            model_name='catmissionr',
            name='nb_days',
            field=models.PositiveIntegerField(default=0),
        ),
        migrations.AddField(
            model_name='catmissionr',
            name='result_delay_max',
            field=models.PositiveIntegerField(default=0),
        ),
        migrations.AddField(
            model_name='catmissionr',
            name='result_delay_mean',
            field=models.FloatField(default=0),
        ),
        migrations.AddField(
            model_name='catmissionr',
            name='result_delay_median',
            field=models.FloatField(default=0),
        ),
        migrations.AddField(
            model_name='catmissionr',
            name='result_delay_min',
            field=models.PositiveIntegerField(default=0),
        ),
        migrations.AddField(
            model_name='catmissionr',
            name='result_delay_total',
            field=models.PositiveIntegerField(default=0),
        ),
    ]
