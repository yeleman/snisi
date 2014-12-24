# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('snisi_nutrition', '0006_auto_20141224_1036'),
    ]

    operations = [
        migrations.AlterField(
            model_name='aggweeklynutritionr',
            name='urenam_cases',
            field=models.PositiveIntegerField(default=0, verbose_name='MAM Cases'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='aggweeklynutritionr',
            name='urenam_deaths',
            field=models.PositiveIntegerField(default=0, verbose_name='MAM Deaths'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='aggweeklynutritionr',
            name='urenam_screening',
            field=models.PositiveIntegerField(default=0, verbose_name='MAM Screening'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='aggweeklynutritionr',
            name='urenas_cases',
            field=models.PositiveIntegerField(default=0, verbose_name='SAM Cases'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='aggweeklynutritionr',
            name='urenas_deaths',
            field=models.PositiveIntegerField(default=0, verbose_name='SAM Deaths'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='aggweeklynutritionr',
            name='urenas_screening',
            field=models.PositiveIntegerField(default=0, verbose_name='SAM Screening'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='aggweeklynutritionr',
            name='ureni_cases',
            field=models.PositiveIntegerField(default=0, verbose_name='SAM+ Cases'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='aggweeklynutritionr',
            name='ureni_deaths',
            field=models.PositiveIntegerField(default=0, verbose_name='SAM+ Deaths'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='aggweeklynutritionr',
            name='ureni_screening',
            field=models.PositiveIntegerField(default=0, verbose_name='SAM+ Screening'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='weeklynutritionr',
            name='urenam_cases',
            field=models.PositiveIntegerField(default=0, verbose_name='MAM Cases'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='weeklynutritionr',
            name='urenam_deaths',
            field=models.PositiveIntegerField(default=0, verbose_name='MAM Deaths'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='weeklynutritionr',
            name='urenam_screening',
            field=models.PositiveIntegerField(default=0, verbose_name='MAM Screening'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='weeklynutritionr',
            name='urenas_cases',
            field=models.PositiveIntegerField(default=0, verbose_name='SAM Cases'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='weeklynutritionr',
            name='urenas_deaths',
            field=models.PositiveIntegerField(default=0, verbose_name='SAM Deaths'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='weeklynutritionr',
            name='urenas_screening',
            field=models.PositiveIntegerField(default=0, verbose_name='SAM Screening'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='weeklynutritionr',
            name='ureni_cases',
            field=models.PositiveIntegerField(default=0, verbose_name='SAM+ Cases'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='weeklynutritionr',
            name='ureni_deaths',
            field=models.PositiveIntegerField(default=0, verbose_name='SAM+ Deaths'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='weeklynutritionr',
            name='ureni_screening',
            field=models.PositiveIntegerField(default=0, verbose_name='SAM+ Screening'),
            preserve_default=True,
        ),
    ]
