# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('snisi_reprohealth', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='aggpfactivitiesr',
            name='emergency_controls_initial',
            field=models.PositiveIntegerField(default=0, verbose_name='Emergency Controls: Initial Quantity'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='aggpfactivitiesr',
            name='emergency_controls_lost',
            field=models.PositiveIntegerField(default=0, verbose_name='Emergency Controls: Quantity Lost'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='aggpfactivitiesr',
            name='emergency_controls_received',
            field=models.PositiveIntegerField(default=0, verbose_name='Emergency Controls: Quantity Received'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='aggpfactivitiesr',
            name='emergency_controls_removal_price',
            field=models.PositiveIntegerField(default=0, verbose_name='Emergency Controls: Price'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='aggpfactivitiesr',
            name='emergency_controls_removal_qty',
            field=models.PositiveIntegerField(default=0, verbose_name='Emergency Controls: Quantity'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='aggpfactivitiesr',
            name='emergency_controls_removal_revenue',
            field=models.PositiveIntegerField(default=0, verbose_name='Emergency Controls'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='aggpfactivitiesr',
            name='emergency_controls_used',
            field=models.PositiveIntegerField(default=0, verbose_name='Emergency Controls: Quantity Used'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='pfactivitiesr',
            name='emergency_controls_initial',
            field=models.PositiveIntegerField(default=0, verbose_name='Emergency Controls: Initial Quantity'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='pfactivitiesr',
            name='emergency_controls_lost',
            field=models.PositiveIntegerField(default=0, verbose_name='Emergency Controls: Quantity Lost'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='pfactivitiesr',
            name='emergency_controls_observation',
            field=models.CharField(max_length=500, null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='pfactivitiesr',
            name='emergency_controls_received',
            field=models.PositiveIntegerField(default=0, verbose_name='Emergency Controls: Quantity Received'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='pfactivitiesr',
            name='emergency_controls_removal_price',
            field=models.PositiveIntegerField(default=0, verbose_name='Emergency Controls: Price'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='pfactivitiesr',
            name='emergency_controls_removal_qty',
            field=models.PositiveIntegerField(default=0, verbose_name='Emergency Controls: Quantity'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='pfactivitiesr',
            name='emergency_controls_removal_revenue',
            field=models.PositiveIntegerField(default=0, verbose_name='Emergency Controls'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='pfactivitiesr',
            name='emergency_controls_used',
            field=models.PositiveIntegerField(default=0, verbose_name='Emergency Controls: Quantity Used'),
            preserve_default=False,
        ),
    ]
