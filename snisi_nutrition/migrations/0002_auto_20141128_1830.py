# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('snisi_nutrition', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='aggurenamnutritionr',
            name='exsam_referred',
        ),
        migrations.RemoveField(
            model_name='urenamnutritionr',
            name='exsam_referred',
        ),
        migrations.AddField(
            model_name='aggurenamnutritionr',
            name='exsam_grand_total_in',
            field=models.PositiveIntegerField(default=0, verbose_name='[Ex-SAM] Grand Total In'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='urenamnutritionr',
            name='exsam_grand_total_in',
            field=models.PositiveIntegerField(default=0, verbose_name='[Ex-SAM] Grand Total In'),
            preserve_default=False,
        ),
    ]
