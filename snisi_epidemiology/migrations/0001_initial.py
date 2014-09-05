# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('snisi_core', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='AggEpidemiologyR',
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
                ('ebola_case', models.IntegerField(verbose_name='Ebola cases')),
                ('ebola_death', models.IntegerField(verbose_name='Ebola death')),
                ('acute_flaccid_paralysis_case', models.IntegerField(verbose_name='AFP cases')),
                ('acute_flaccid_paralysis_death', models.IntegerField(verbose_name='AFP death')),
                ('influenza_a_h1n1_case', models.IntegerField(verbose_name='Influenza A H1N1 cases')),
                ('influenza_a_h1n1_death', models.IntegerField(verbose_name='Influenza A H1N1 death')),
                ('cholera_case', models.IntegerField(verbose_name='Cholera cases')),
                ('cholera_death', models.IntegerField(verbose_name='Cholera death')),
                ('red_diarrhea_case', models.IntegerField(verbose_name='Red Diarrhea cases')),
                ('red_diarrhea_death', models.IntegerField(verbose_name='Red Diarrhea death')),
                ('measles_case', models.IntegerField(verbose_name='Measles cases')),
                ('measles_death', models.IntegerField(verbose_name='Measles death')),
                ('yellow_fever_case', models.IntegerField(verbose_name='Yellow Fever cases')),
                ('yellow_fever_death', models.IntegerField(verbose_name='Yellow Fever death')),
                ('neonatal_tetanus_case', models.IntegerField(verbose_name='NNT cases')),
                ('neonatal_tetanus_death', models.IntegerField(verbose_name='NNT death')),
                ('meningitis_case', models.IntegerField(verbose_name='Meningitis cases')),
                ('meningitis_death', models.IntegerField(verbose_name='Meningitis death')),
                ('rabies_case', models.IntegerField(verbose_name='Rabies cases')),
                ('rabies_death', models.IntegerField(verbose_name='Rabies death')),
                ('acute_measles_diarrhea_case', models.IntegerField(verbose_name='Acute Measles Diarrhea cases')),
                ('acute_measles_diarrhea_death', models.IntegerField(verbose_name='Acute Measles Diarrhea death')),
                ('other_notifiable_disease_case', models.IntegerField(verbose_name='Other Notifiable Diseases cases')),
                ('other_notifiable_disease_death', models.IntegerField(verbose_name='Other Notifiable Diseases death')),
                ('agg_sources', models.ManyToManyField(related_name='aggregated_agg_aggepidemiologyr_reports', null=True, verbose_name='Aggr. Sources (all)', to='snisi_epidemiology.AggEpidemiologyR', blank=True)),
                ('direct_agg_sources', models.ManyToManyField(related_name='direct_aggregated_agg_aggepidemiologyr_reports', null=True, verbose_name='Aggr. Sources (direct)', to='snisi_epidemiology.AggEpidemiologyR', blank=True)),
            ],
            options={
                'verbose_name': 'Aggregated Epidemiology Report',
                'verbose_name_plural': 'Aggregated Epidemiology Reports',
            },
            bases=('snisi_core.snisireport', models.Model),
        ),
        migrations.CreateModel(
            name='EpidemiologyR',
            fields=[
                ('snisireport_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='snisi_core.SNISIReport')),
                ('ebola_case', models.IntegerField(verbose_name='Ebola cases')),
                ('ebola_death', models.IntegerField(verbose_name='Ebola death')),
                ('acute_flaccid_paralysis_case', models.IntegerField(verbose_name='AFP cases')),
                ('acute_flaccid_paralysis_death', models.IntegerField(verbose_name='AFP death')),
                ('influenza_a_h1n1_case', models.IntegerField(verbose_name='Influenza A H1N1 cases')),
                ('influenza_a_h1n1_death', models.IntegerField(verbose_name='Influenza A H1N1 death')),
                ('cholera_case', models.IntegerField(verbose_name='Cholera cases')),
                ('cholera_death', models.IntegerField(verbose_name='Cholera death')),
                ('red_diarrhea_case', models.IntegerField(verbose_name='Red Diarrhea cases')),
                ('red_diarrhea_death', models.IntegerField(verbose_name='Red Diarrhea death')),
                ('measles_case', models.IntegerField(verbose_name='Measles cases')),
                ('measles_death', models.IntegerField(verbose_name='Measles death')),
                ('yellow_fever_case', models.IntegerField(verbose_name='Yellow Fever cases')),
                ('yellow_fever_death', models.IntegerField(verbose_name='Yellow Fever death')),
                ('neonatal_tetanus_case', models.IntegerField(verbose_name='NNT cases')),
                ('neonatal_tetanus_death', models.IntegerField(verbose_name='NNT death')),
                ('meningitis_case', models.IntegerField(verbose_name='Meningitis cases')),
                ('meningitis_death', models.IntegerField(verbose_name='Meningitis death')),
                ('rabies_case', models.IntegerField(verbose_name='Rabies cases')),
                ('rabies_death', models.IntegerField(verbose_name='Rabies death')),
                ('acute_measles_diarrhea_case', models.IntegerField(verbose_name='Acute Measles Diarrhea cases')),
                ('acute_measles_diarrhea_death', models.IntegerField(verbose_name='Acute Measles Diarrhea death')),
                ('other_notifiable_disease_case', models.IntegerField(verbose_name='Other Notifiable Diseases cases')),
                ('other_notifiable_disease_death', models.IntegerField(verbose_name='Other Notifiable Diseases death')),
            ],
            options={
                'verbose_name': 'Epidemiology Report',
                'verbose_name_plural': 'Epidemiology Reports',
            },
            bases=('snisi_core.snisireport',),
        ),
        migrations.AddField(
            model_name='aggepidemiologyr',
            name='indiv_sources',
            field=models.ManyToManyField(related_name='source_agg_aggepidemiologyr_reports', null=True, verbose_name='Primary. Sources', to='snisi_epidemiology.EpidemiologyR', blank=True),
            preserve_default=True,
        ),
        migrations.CreateModel(
            name='EpiWeekDistrictValidationPeriod',
            fields=[
            ],
            options={
                'verbose_name': 'Week District Validation Period',
                'proxy': True,
                'verbose_name_plural': 'Week District Validation Periods',
            },
            bases=('snisi_core.weekperiod',),
        ),
        migrations.CreateModel(
            name='EpiWeekPeriod',
            fields=[
            ],
            options={
                'verbose_name': 'Week Period',
                'proxy': True,
                'verbose_name_plural': 'Week Periods',
            },
            bases=('snisi_core.weekperiod',),
        ),
        migrations.CreateModel(
            name='EpiWeekRegionValidationPeriod',
            fields=[
            ],
            options={
                'verbose_name': 'Week Region Validation Period',
                'proxy': True,
                'verbose_name_plural': 'Week Region Validation Periods',
            },
            bases=('snisi_core.weekperiod',),
        ),
        migrations.CreateModel(
            name='EpiWeekReportingPeriod',
            fields=[
            ],
            options={
                'verbose_name': 'Week Reporting Period',
                'proxy': True,
                'verbose_name_plural': 'Week Reporting Periods',
            },
            bases=('snisi_core.weekperiod',),
        ),
    ]
