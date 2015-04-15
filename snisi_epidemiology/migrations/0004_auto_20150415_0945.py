# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('snisi_epidemiology', '0003_epidemiologyalertr'),
    ]

    operations = [
        migrations.AlterField(
            model_name='aggepidemiologyr',
            name='agg_sources',
            field=models.ManyToManyField(related_name='aggregated_agg_aggepidemiologyr_reports', verbose_name='Aggr. Sources (all)', to='snisi_epidemiology.AggEpidemiologyR', blank=True),
        ),
        migrations.AlterField(
            model_name='aggepidemiologyr',
            name='direct_agg_sources',
            field=models.ManyToManyField(related_name='direct_aggregated_agg_aggepidemiologyr_reports', verbose_name='Aggr. Sources (direct)', to='snisi_epidemiology.AggEpidemiologyR', blank=True),
        ),
        migrations.AlterField(
            model_name='aggepidemiologyr',
            name='indiv_sources',
            field=models.ManyToManyField(related_name='source_agg_aggepidemiologyr_reports', verbose_name='Primary. Sources', to='snisi_epidemiology.EpidemiologyR', blank=True),
        ),
    ]
