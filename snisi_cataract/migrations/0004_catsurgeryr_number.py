# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('snisi_cataract', '0003_auto_20160204_1145'),
    ]

    operations = [
        migrations.AddField(
            model_name='catsurgeryr',
            name='number',
            field=models.PositiveIntegerField(default=1),
            preserve_default=False,
        ),
    ]
