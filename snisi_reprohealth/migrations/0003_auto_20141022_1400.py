# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('snisi_reprohealth', '0002_auto_20141008_1709'),
    ]

    operations = [
        migrations.RenameField(
            model_name='aggpfactivitiesr',
            old_name='emergency_controls_removal_price',
            new_name='emergency_controls_price',
        ),
        migrations.RenameField(
            model_name='aggpfactivitiesr',
            old_name='emergency_controls_removal_qty',
            new_name='emergency_controls_qty',
        ),
        migrations.RenameField(
            model_name='aggpfactivitiesr',
            old_name='emergency_controls_removal_revenue',
            new_name='emergency_controls_revenue',
        ),
        migrations.RenameField(
            model_name='pfactivitiesr',
            old_name='emergency_controls_removal_price',
            new_name='emergency_controls_price',
        ),
        migrations.RenameField(
            model_name='pfactivitiesr',
            old_name='emergency_controls_removal_qty',
            new_name='emergency_controls_qty',
        ),
        migrations.RenameField(
            model_name='pfactivitiesr',
            old_name='emergency_controls_removal_revenue',
            new_name='emergency_controls_revenue',
        ),
    ]
