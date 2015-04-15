# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('snisi_malaria', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='aggepidemiomalariar',
            name='agg_sources',
            field=models.ManyToManyField(related_name='aggregated_agg_aggepidemiomalariar_reports', verbose_name='Aggr. Sources (all)', to='snisi_malaria.AggEpidemioMalariaR', blank=True),
        ),
        migrations.AlterField(
            model_name='aggepidemiomalariar',
            name='direct_agg_sources',
            field=models.ManyToManyField(related_name='direct_aggregated_agg_aggepidemiomalariar_reports', verbose_name='Aggr. Sources (direct)', to='snisi_malaria.AggEpidemioMalariaR', blank=True),
        ),
        migrations.AlterField(
            model_name='aggepidemiomalariar',
            name='direct_indiv_sources',
            field=models.ManyToManyField(related_name='direct_source_agg_aggepidemiomalariar_reports', verbose_name='Primary. Sources (direct)', to='snisi_malaria.EpidemioMalariaR', blank=True),
        ),
        # migrations.AlterField(
        #     model_name='aggepidemiomalariar',
        #     name='indiv_sources',
        #     field=models.ManyToManyField(related_name='source_agg_aggepidemiomalariar_reports', verbose_name='Primary. Sources (all)', to='snisi_malaria.EpidemioMalariaR', blank=True),
        # ),
        migrations.AlterField(
            model_name='aggmalariar',
            name='agg_sources',
            field=models.ManyToManyField(related_name='aggregated_agg_aggmalariar_reports', verbose_name='Aggr. Sources (all)', to='snisi_malaria.AggMalariaR', blank=True),
        ),
        migrations.AlterField(
            model_name='aggmalariar',
            name='direct_agg_sources',
            field=models.ManyToManyField(related_name='direct_aggregated_agg_aggmalariar_reports', verbose_name='Aggr. Sources (direct)', to='snisi_malaria.AggMalariaR', blank=True),
        ),
        migrations.AlterField(
            model_name='aggmalariar',
            name='direct_indiv_sources',
            field=models.ManyToManyField(related_name='direct_source_agg_aggmalariar_reports', verbose_name='Primary. Sources (direct)', to='snisi_malaria.MalariaR', blank=True),
        ),
        migrations.AlterField(
            model_name='aggmalariar',
            name='indiv_sources',
            field=models.ManyToManyField(related_name='source_agg_aggmalariar_reports', verbose_name='Primary. Sources (all)', to='snisi_malaria.MalariaR', blank=True),
        ),
    ]
