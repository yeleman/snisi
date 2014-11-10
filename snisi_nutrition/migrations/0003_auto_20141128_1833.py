# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('snisi_nutrition', '0002_auto_20141128_1830'),
    ]

    operations = [
        migrations.AddField(
            model_name='aggurenamnutritionr',
            name='exsam_grand_total_out',
            field=models.PositiveIntegerField(default=0, verbose_name='[Ex-SAM] Grand Total Out'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='urenamnutritionr',
            name='exsam_grand_total_out',
            field=models.PositiveIntegerField(default=0, verbose_name='[Ex-SAM] Grand Total Out'),
            preserve_default=False,
        ),
    ]
