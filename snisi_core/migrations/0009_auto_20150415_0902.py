# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('snisi_core', '0008_auto_20150415_0945'),
    ]

    operations = [
        migrations.AlterField(
            model_name='expectedvalidation',
            name='report',
            field=models.OneToOneField(related_name='expected_validation', primary_key=True, serialize=False, to='snisi_core.SNISIReport'),
        ),
    ]
