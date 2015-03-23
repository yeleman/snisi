# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('snisi_core', '0005_auto_20150205_1516'),
    ]

    operations = [
        migrations.AddField(
            model_name='entitytype',
            name='short_name',
            field=models.CharField(max_length=10, null=True, verbose_name='Name', blank=True),
            preserve_default=True,
        ),
    ]
