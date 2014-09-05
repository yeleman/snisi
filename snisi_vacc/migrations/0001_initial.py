# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('snisi_core', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='AggVaccCovR',
            fields=[
                ('snisireport_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='snisi_core.SNISIReport')),
                ('nb_source_reports_expected', models.PositiveIntegerField(null=True, blank=True)),
                ('nb_source_reports_arrived', models.PositiveIntegerField(null=True, blank=True)),
                ('nb_source_reports_arrived_on_time', models.PositiveIntegerField(null=True, blank=True)),
                ('nb_source_reports_arrived_correct', models.PositiveIntegerField(null=True, blank=True)),
                ('nb_source_reports_arrived_complete', models.PositiveIntegerField(null=True, blank=True)),
                ('nb_source_reports_altered', models.PositiveIntegerField(null=True, blank=True)),
                ('nb_source_reports_validated', models.PositiveIntegerField(null=True, blank=True)),
                ('nb_source_reports_auto_validated', models.PositiveIntegerField(null=True, blank=True)),
                ('nb_agg_reports_altered', models.PositiveIntegerField(null=True, blank=True)),
                ('nb_agg_reports_validated', models.PositiveIntegerField(null=True, blank=True)),
                ('nb_agg_reports_auto_validated', models.PositiveIntegerField(null=True, blank=True)),
                ('bcg_coverage', models.FloatField(verbose_name='BCG Coverage')),
                ('polio3_coverage', models.FloatField(verbose_name='Penta3 Coverage')),
                ('measles_coverage', models.FloatField(verbose_name='Measles Coverage')),
                ('polio3_abandonment_rate', models.FloatField(verbose_name='Penta3 Abandonment Rate')),
                ('agg_sources', models.ManyToManyField(related_name='aggregated_agg_aggvacccovr_reports', null=True, verbose_name='Aggr. Sources (all)', to='snisi_vacc.AggVaccCovR', blank=True)),
                ('direct_agg_sources', models.ManyToManyField(related_name='direct_aggregated_agg_aggvacccovr_reports', null=True, verbose_name='Aggr. Sources (direct)', to='snisi_vacc.AggVaccCovR', blank=True)),
            ],
            options={
                'verbose_name': 'Aggregated Major Vaccine Coverage Report',
                'verbose_name_plural': 'Aggregated Major Vaccine Coverage Reports',
            },
            bases=('snisi_core.snisireport', models.Model),
        ),
        migrations.CreateModel(
            name='VaccCovR',
            fields=[
                ('snisireport_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='snisi_core.SNISIReport')),
                ('bcg_coverage', models.FloatField(verbose_name='BCG Coverage')),
                ('polio3_coverage', models.FloatField(verbose_name='Penta3 Coverage')),
                ('measles_coverage', models.FloatField(verbose_name='Measles Coverage')),
                ('polio3_abandonment_rate', models.FloatField(verbose_name='Penta3 Abandonment Rate')),
            ],
            options={
                'verbose_name': 'Provided Services Report',
                'verbose_name_plural': 'Provided Services Reports',
            },
            bases=('snisi_core.snisireport', models.Model),
        ),
        migrations.AddField(
            model_name='aggvacccovr',
            name='direct_indiv_sources',
            field=models.ManyToManyField(related_name='direct_source_agg_aggvacccovr_reports', null=True, verbose_name='Primary. Sources (direct)', to='snisi_vacc.VaccCovR', blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='aggvacccovr',
            name='indiv_sources',
            field=models.ManyToManyField(related_name='source_agg_aggvacccovr_reports', null=True, verbose_name='Primary. Sources (all)', to='snisi_vacc.VaccCovR', blank=True),
            preserve_default=True,
        ),
    ]
