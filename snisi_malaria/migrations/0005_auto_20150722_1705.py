# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('snisi_core', '0010_auto_20150710_1405'),
        ('snisi_malaria', '0004_auto_20150710_1453'),
    ]

    operations = [
        migrations.CreateModel(
            name='AggWeeklyMalariaR',
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
                ('day1_u5_total_confirmed_malaria_cases', models.PositiveIntegerField(verbose_name='Total Confirmed Malaria Cases')),
                ('day1_o5_total_confirmed_malaria_cases', models.PositiveIntegerField(verbose_name='Total Confirmed Malaria Cases')),
                ('day1_pw_total_confirmed_malaria_cases', models.PositiveIntegerField(verbose_name='Total Confirmed Malaria Cases')),
                ('day2_u5_total_confirmed_malaria_cases', models.PositiveIntegerField(verbose_name='Total Confirmed Malaria Cases')),
                ('day2_o5_total_confirmed_malaria_cases', models.PositiveIntegerField(verbose_name='Total Confirmed Malaria Cases')),
                ('day2_pw_total_confirmed_malaria_cases', models.PositiveIntegerField(verbose_name='Total Confirmed Malaria Cases')),
                ('day3_u5_total_confirmed_malaria_cases', models.PositiveIntegerField(verbose_name='Total Confirmed Malaria Cases')),
                ('day3_o5_total_confirmed_malaria_cases', models.PositiveIntegerField(verbose_name='Total Confirmed Malaria Cases')),
                ('day3_pw_total_confirmed_malaria_cases', models.PositiveIntegerField(verbose_name='Total Confirmed Malaria Cases')),
                ('day4_u5_total_confirmed_malaria_cases', models.PositiveIntegerField(verbose_name='Total Confirmed Malaria Cases')),
                ('day4_o5_total_confirmed_malaria_cases', models.PositiveIntegerField(verbose_name='Total Confirmed Malaria Cases')),
                ('day4_pw_total_confirmed_malaria_cases', models.PositiveIntegerField(verbose_name='Total Confirmed Malaria Cases')),
                ('day5_u5_total_confirmed_malaria_cases', models.PositiveIntegerField(verbose_name='Total Confirmed Malaria Cases')),
                ('day5_o5_total_confirmed_malaria_cases', models.PositiveIntegerField(verbose_name='Total Confirmed Malaria Cases')),
                ('day5_pw_total_confirmed_malaria_cases', models.PositiveIntegerField(verbose_name='Total Confirmed Malaria Cases')),
                ('day6_u5_total_confirmed_malaria_cases', models.PositiveIntegerField(verbose_name='Total Confirmed Malaria Cases')),
                ('day6_o5_total_confirmed_malaria_cases', models.PositiveIntegerField(verbose_name='Total Confirmed Malaria Cases')),
                ('day6_pw_total_confirmed_malaria_cases', models.PositiveIntegerField(verbose_name='Total Confirmed Malaria Cases')),
                ('day7_u5_total_confirmed_malaria_cases', models.PositiveIntegerField(verbose_name='Total Confirmed Malaria Cases')),
                ('day7_o5_total_confirmed_malaria_cases', models.PositiveIntegerField(verbose_name='Total Confirmed Malaria Cases')),
                ('day7_pw_total_confirmed_malaria_cases', models.PositiveIntegerField(verbose_name='Total Confirmed Malaria Cases')),
                ('u5_total_confirmed_malaria_cases', models.PositiveIntegerField(verbose_name='Total Confirmed Malaria Cases')),
                ('o5_total_confirmed_malaria_cases', models.PositiveIntegerField(verbose_name='Total Confirmed Malaria Cases')),
                ('pw_total_confirmed_malaria_cases', models.PositiveIntegerField(verbose_name='Total Confirmed Malaria Cases')),
                ('agg_sources', models.ManyToManyField(related_name='aggregated_agg_aggweeklymalariar_reports', verbose_name='Aggr. Sources (all)', to='snisi_malaria.AggWeeklyMalariaR', blank=True)),
                ('direct_agg_sources', models.ManyToManyField(related_name='direct_aggregated_agg_aggweeklymalariar_reports', verbose_name='Aggr. Sources (direct)', to='snisi_malaria.AggWeeklyMalariaR', blank=True)),
            ],
            options={
                'verbose_name': 'Aggregated Weekly Malaria Report',
                'verbose_name_plural': 'Aggregated Weekly Malaria Reports',
            },
            bases=('snisi_core.snisireport', models.Model),
        ),
        migrations.AlterModelOptions(
            name='aggdailymalariar',
            options={'verbose_name': 'Aggregated Daily Malaria Report', 'verbose_name_plural': 'Aggregated Daily Malaria Reports'},
        ),
        migrations.AlterModelOptions(
            name='dailymalariar',
            options={'verbose_name': 'Daily Malaria Report', 'verbose_name_plural': 'Daily Malaria Reports'},
        ),
        migrations.AddField(
            model_name='aggweeklymalariar',
            name='direct_indiv_sources',
            field=models.ManyToManyField(related_name='direct_source_agg_aggweeklymalariar_reports', verbose_name='Primary. Sources (direct)', to='snisi_malaria.DailyMalariaR', blank=True),
        ),
        migrations.AddField(
            model_name='aggweeklymalariar',
            name='indiv_sources',
            field=models.ManyToManyField(related_name='source_agg_aggweeklymalariar_reports', verbose_name='Primary. Sources (all)', to='snisi_malaria.DailyMalariaR', blank=True),
        ),
    ]
