# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('snisi_core', '0010_auto_20150710_1405'),
        ('snisi_malaria', '0003_auto_20150526_0941'),
    ]

    operations = [
        migrations.CreateModel(
            name='AggDailyMalariaR',
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
                ('u5_total_confirmed_malaria_cases', models.PositiveIntegerField(verbose_name='Total Confirmed Malaria Cases')),
                ('o5_total_confirmed_malaria_cases', models.PositiveIntegerField(verbose_name='Total Confirmed Malaria Cases')),
                ('pw_total_confirmed_malaria_cases', models.PositiveIntegerField(verbose_name='Total Confirmed Malaria Cases')),
                ('agg_sources', models.ManyToManyField(related_name='aggregated_agg_aggdailymalariar_reports', verbose_name='Aggr. Sources (all)', to='snisi_malaria.AggDailyMalariaR', blank=True)),
                ('direct_agg_sources', models.ManyToManyField(related_name='direct_aggregated_agg_aggdailymalariar_reports', verbose_name='Aggr. Sources (direct)', to='snisi_malaria.AggDailyMalariaR', blank=True)),
            ],
            options={
                'verbose_name': 'Aggregated Weekly Malaria Report',
                'verbose_name_plural': 'Aggregated Weekly Malaria Reports',
            },
            bases=('snisi_core.snisireport', models.Model),
        ),
        migrations.CreateModel(
            name='DailyMalariaR',
            fields=[
                ('snisireport_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='snisi_core.SNISIReport')),
                ('u5_total_confirmed_malaria_cases', models.PositiveIntegerField(verbose_name='Total Confirmed Malaria Cases')),
                ('o5_total_confirmed_malaria_cases', models.PositiveIntegerField(verbose_name='Total Confirmed Malaria Cases')),
                ('pw_total_confirmed_malaria_cases', models.PositiveIntegerField(verbose_name='Total Confirmed Malaria Cases')),
            ],
            options={
                'verbose_name': 'Weekly Malaria Report',
                'verbose_name_plural': 'Weekly Malaria Reports',
            },
            bases=('snisi_core.snisireport', models.Model),
        ),
        migrations.AddField(
            model_name='aggdailymalariar',
            name='direct_indiv_sources',
            field=models.ManyToManyField(related_name='direct_source_agg_aggdailymalariar_reports', verbose_name='Primary. Sources (direct)', to='snisi_malaria.DailyMalariaR', blank=True),
        ),
        migrations.AddField(
            model_name='aggdailymalariar',
            name='indiv_sources',
            field=models.ManyToManyField(related_name='source_agg_aggdailymalariar_reports', verbose_name='Primary. Sources (all)', to='snisi_malaria.DailyMalariaR', blank=True),
        ),
    ]
