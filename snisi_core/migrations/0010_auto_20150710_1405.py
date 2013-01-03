# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('snisi_core', '0009_auto_20150415_0902'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='snisireport',
            options={'ordering': ('period__start_on',)},
        ),
    ]
