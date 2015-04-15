# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('snisi_trachoma', '0002_auto_20140905_1608'),
    ]

    operations = [
        migrations.AlterField(
            model_name='aggttbacklogmissionr',
            name='agg_sources',
            field=models.ManyToManyField(related_name='aggregated_agg_aggttbacklogmissionr_reports', verbose_name='Aggr. Sources (all)', to='snisi_trachoma.AggTTBacklogMissionR', blank=True),
        ),
        migrations.AlterField(
            model_name='aggttbacklogmissionr',
            name='direct_agg_sources',
            field=models.ManyToManyField(related_name='direct_aggregated_agg_aggttbacklogmissionr_reports', verbose_name='Aggr. Sources (direct)', to='snisi_trachoma.AggTTBacklogMissionR', blank=True),
        ),
        migrations.AlterField(
            model_name='aggttbacklogmissionr',
            name='village_reports',
            field=models.ManyToManyField(to='snisi_trachoma.TTBacklogVillageR', verbose_name='Rapports Villages', blank=True),
        ),
        migrations.AlterField(
            model_name='ttbacklogmissionr',
            name='village_reports',
            field=models.ManyToManyField(to='snisi_trachoma.TTBacklogVillageR', verbose_name='Rapports Villages', blank=True),
        ),
    ]
