# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('snisi_core', '0003_auto_20141117_1551'),
    ]

    operations = [
        migrations.AlterField(
            model_name='expectedreporting',
            name='completion_status',
            field=models.CharField(default='missing', max_length=30, choices=[('missing', 'Missing'), ('satisfied', 'Complete'), ('matching', 'Matching')]),
            preserve_default=True,
        ),
    ]
