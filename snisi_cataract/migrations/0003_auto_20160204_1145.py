# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('snisi_cataract', '0002_auto_20160203_1633'),
    ]

    operations = [
        migrations.AlterField(
            model_name='catmissionr',
            name='operator',
            field=models.ForeignKey(verbose_name='Operator', to=settings.AUTH_USER_MODEL, null=True),
        ),
        migrations.AlterField(
            model_name='catmissionr',
            name='operator_type',
            field=models.CharField(max_length=75, null=True, verbose_name='Operatr Profile', choices=[('OPT', 'OPT'), ('TSO', 'TSO'), ('AMO', 'AMO')]),
        ),
        migrations.AlterField(
            model_name='catsurgeryr',
            name='gender',
            field=models.CharField(max_length=20, choices=[('male', 'Male'), ('female', 'FEMALE')]),
        ),
    ]
