# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('snisi_trachoma', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='aggttbacklogmissionr',
            name='community_assistance',
            field=models.PositiveIntegerField(verbose_name='Assistance relais'),
        ),
    ]
