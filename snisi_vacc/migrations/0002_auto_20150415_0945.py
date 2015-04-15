# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('snisi_vacc', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='aggvacccovr',
            name='agg_sources',
            field=models.ManyToManyField(related_name='aggregated_agg_aggvacccovr_reports', verbose_name='Aggr. Sources (all)', to='snisi_vacc.AggVaccCovR', blank=True),
        ),
        migrations.AlterField(
            model_name='aggvacccovr',
            name='direct_agg_sources',
            field=models.ManyToManyField(related_name='direct_aggregated_agg_aggvacccovr_reports', verbose_name='Aggr. Sources (direct)', to='snisi_vacc.AggVaccCovR', blank=True),
        ),
        migrations.AlterField(
            model_name='aggvacccovr',
            name='direct_indiv_sources',
            field=models.ManyToManyField(related_name='direct_source_agg_aggvacccovr_reports', verbose_name='Primary. Sources (direct)', to='snisi_vacc.VaccCovR', blank=True),
        ),
        migrations.AlterField(
            model_name='aggvacccovr',
            name='indiv_sources',
            field=models.ManyToManyField(related_name='source_agg_aggvacccovr_reports', verbose_name='Primary. Sources (all)', to='snisi_vacc.VaccCovR', blank=True),
        ),
    ]
