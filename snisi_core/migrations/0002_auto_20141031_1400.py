# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('snisi_core', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='healthentity',
            name='has_urenam',
            field=models.BooleanField(default=False),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='healthentity',
            name='has_urenas',
            field=models.BooleanField(default=False),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='healthentity',
            name='has_ureni',
            field=models.BooleanField(default=False),
            preserve_default=True,
        ),
    ]
