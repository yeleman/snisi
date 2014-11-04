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
            name='exsam_total_out_f',
        ),
        migrations.RemoveField(
            model_name='aggurenamnutritionr',
            name='exsam_total_out_m',
        ),
        migrations.RemoveField(
            model_name='urenamnutritionr',
            name='exsam_total_out_f',
        ),
        migrations.RemoveField(
            model_name='urenamnutritionr',
            name='exsam_total_out_m',
        ),
        migrations.AddField(
            model_name='aggurenamnutritionr',
            name='o59_not_responding',
            field=models.PositiveIntegerField(default=0, verbose_name='[59m+] Not Responding'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='aggurenamnutritionr',
            name='pw_not_responding',
            field=models.PositiveIntegerField(default=0, verbose_name='[PW/BF] Not Responding'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='aggurenamnutritionr',
            name='u23o6_not_responding',
            field=models.PositiveIntegerField(default=0, verbose_name='[6-23m] Not Responding'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='aggurenamnutritionr',
            name='u59o23_not_responding',
            field=models.PositiveIntegerField(default=0, verbose_name='[23-59m] Not Responding'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='aggurenasnutritionr',
            name='o59_not_responding',
            field=models.PositiveIntegerField(default=0, verbose_name='[59m+] Not Responding'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='aggurenasnutritionr',
            name='u59o6_not_responding',
            field=models.PositiveIntegerField(default=0, verbose_name='[6-59m] Not Responding'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='urenamnutritionr',
            name='o59_not_responding',
            field=models.PositiveIntegerField(default=0, verbose_name='[59m+] Not Responding'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='urenamnutritionr',
            name='pw_not_responding',
            field=models.PositiveIntegerField(default=0, verbose_name='[PW/BF] Not Responding'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='urenamnutritionr',
            name='u23o6_not_responding',
            field=models.PositiveIntegerField(default=0, verbose_name='[6-23m] Not Responding'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='urenamnutritionr',
            name='u59o23_not_responding',
            field=models.PositiveIntegerField(default=0, verbose_name='[23-59m] Not Responding'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='urenasnutritionr',
            name='o59_not_responding',
            field=models.PositiveIntegerField(default=0, verbose_name='[59m+] Not Responding'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='urenasnutritionr',
            name='u59o6_not_responding',
            field=models.PositiveIntegerField(default=0, verbose_name='[6-59m] Not Responding'),
            preserve_default=False,
        ),
    ]
