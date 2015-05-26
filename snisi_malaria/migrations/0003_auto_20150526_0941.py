# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('snisi_malaria', '0002_auto_20150415_1037'),
    ]

    operations = [
        migrations.AddField(
            model_name='aggmalariar',
            name='pw_total_simple_malaria_cases',
            field=models.PositiveIntegerField(default=0, verbose_name='Total Simple Malaria Cases'),
        ),
        migrations.AddField(
            model_name='malariar',
            name='pw_total_simple_malaria_cases',
            field=models.PositiveIntegerField(default=0, verbose_name='Total Simple Malaria Cases'),
        ),
    ]
