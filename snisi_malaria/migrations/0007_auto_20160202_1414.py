# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('snisi_malaria', '0006_auto_20130108_0803'),
    ]

    operations = [
        migrations.AlterField(
            model_name='aggdailymalariar',
            name='o5_total_confirmed_malaria_cases',
            field=models.PositiveIntegerField(default=0, verbose_name='Total Confirmed Malaria Cases'),
        ),
        migrations.AlterField(
            model_name='aggdailymalariar',
            name='pw_total_confirmed_malaria_cases',
            field=models.PositiveIntegerField(default=0, verbose_name='Total Confirmed Malaria Cases'),
        ),
        migrations.AlterField(
            model_name='aggdailymalariar',
            name='u5_total_confirmed_malaria_cases',
            field=models.PositiveIntegerField(default=0, verbose_name='Total Confirmed Malaria Cases'),
        ),
        migrations.AlterField(
            model_name='dailymalariar',
            name='o5_total_confirmed_malaria_cases',
            field=models.PositiveIntegerField(default=0, verbose_name='Total Confirmed Malaria Cases'),
        ),
        migrations.AlterField(
            model_name='dailymalariar',
            name='pw_total_confirmed_malaria_cases',
            field=models.PositiveIntegerField(default=0, verbose_name='Total Confirmed Malaria Cases'),
        ),
        migrations.AlterField(
            model_name='dailymalariar',
            name='u5_total_confirmed_malaria_cases',
            field=models.PositiveIntegerField(default=0, verbose_name='Total Confirmed Malaria Cases'),
        ),
    ]
