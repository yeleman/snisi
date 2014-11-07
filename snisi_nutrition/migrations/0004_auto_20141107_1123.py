# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('snisi_nutrition', '0003_auto_20141106_1730'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='aggurenamnutritionr',
            name='pw_total_end_m',
        ),
        migrations.RemoveField(
            model_name='aggurenamnutritionr',
            name='pw_total_in_m',
        ),
        migrations.RemoveField(
            model_name='aggurenamnutritionr',
            name='pw_total_out_m',
        ),
        migrations.RemoveField(
            model_name='aggurenamnutritionr',
            name='pw_total_start_m',
        ),
        migrations.RemoveField(
            model_name='urenamnutritionr',
            name='pw_total_end_m',
        ),
        migrations.RemoveField(
            model_name='urenamnutritionr',
            name='pw_total_in_m',
        ),
        migrations.RemoveField(
            model_name='urenamnutritionr',
            name='pw_total_out_m',
        ),
        migrations.RemoveField(
            model_name='urenamnutritionr',
            name='pw_total_start_m',
        ),
    ]
