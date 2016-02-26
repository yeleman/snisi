# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('snisi_cataract', '0004_catsurgeryr_number'),
    ]

    operations = [
        migrations.AddField(
            model_name='catmissionr',
            name='visual_acuity_max',
            field=models.PositiveIntegerField(default=0),
        ),
        migrations.AddField(
            model_name='catmissionr',
            name='visual_acuity_mean',
            field=models.FloatField(default=0),
        ),
        migrations.AddField(
            model_name='catmissionr',
            name='visual_acuity_median',
            field=models.FloatField(default=0),
        ),
        migrations.AddField(
            model_name='catmissionr',
            name='visual_acuity_min',
            field=models.PositiveIntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='catmissionr',
            name='nb_age_over_50',
            field=models.PositiveIntegerField(default=0, verbose_name='Nb. surgeries Patient over 50'),
        ),
        migrations.AlterField(
            model_name='catmissionr',
            name='nb_age_under_15',
            field=models.PositiveIntegerField(default=0, verbose_name='Nb. surgeries Patient under 15'),
        ),
        migrations.AlterField(
            model_name='catmissionr',
            name='nb_age_under_18',
            field=models.PositiveIntegerField(default=0, verbose_name='Nb. surgeries Patient under 18'),
        ),
        migrations.AlterField(
            model_name='catmissionr',
            name='nb_age_under_20',
            field=models.PositiveIntegerField(default=0, verbose_name='Nb. surgeries Patient under 20'),
        ),
        migrations.AlterField(
            model_name='catmissionr',
            name='nb_age_under_25',
            field=models.PositiveIntegerField(default=0, verbose_name='Nb. surgeries Patient under 25'),
        ),
        migrations.AlterField(
            model_name='catmissionr',
            name='nb_age_under_30',
            field=models.PositiveIntegerField(default=0, verbose_name='Nb. surgeries Patient under 30'),
        ),
        migrations.AlterField(
            model_name='catmissionr',
            name='nb_age_under_35',
            field=models.PositiveIntegerField(default=0, verbose_name='Nb. surgeries Patient under 35'),
        ),
        migrations.AlterField(
            model_name='catmissionr',
            name='nb_age_under_40',
            field=models.PositiveIntegerField(default=0, verbose_name='Nb. surgeries Patient under 40'),
        ),
        migrations.AlterField(
            model_name='catmissionr',
            name='nb_age_under_45',
            field=models.PositiveIntegerField(default=0, verbose_name='Nb. surgeries Patient under 45'),
        ),
        migrations.AlterField(
            model_name='catmissionr',
            name='nb_age_under_50',
            field=models.PositiveIntegerField(default=0, verbose_name='Nb. surgeries Patient under 50'),
        ),
        migrations.AlterField(
            model_name='catmissionr',
            name='nb_surgery_female',
            field=models.PositiveIntegerField(default=0, verbose_name='Nb. surgeries Female'),
        ),
        migrations.AlterField(
            model_name='catmissionr',
            name='nb_surgery_left_eye',
            field=models.PositiveIntegerField(default=0, verbose_name='Nb. surgeries Left Eye'),
        ),
        migrations.AlterField(
            model_name='catmissionr',
            name='nb_surgery_male',
            field=models.PositiveIntegerField(default=0, verbose_name='Nb. surgeries Male'),
        ),
        migrations.AlterField(
            model_name='catmissionr',
            name='nb_surgery_right_eye',
            field=models.PositiveIntegerField(default=0, verbose_name='Nb. surgeries Right Eye'),
        ),
        migrations.AlterField(
            model_name='catsurgeryr',
            name='gender',
            field=models.CharField(max_length=20, choices=[('male', 'Male'), ('female', 'Female')]),
        ),
    ]
