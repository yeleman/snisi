# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('snisi_core', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='AggTTBacklogMissionR',
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
                ('consultation_male', models.PositiveIntegerField(verbose_name='Consultations Hommes')),
                ('consultation_female', models.PositiveIntegerField(verbose_name='Consultations Femmes')),
                ('surgery_male', models.PositiveIntegerField(verbose_name='Chirurgies Hommes')),
                ('surgery_female', models.PositiveIntegerField(verbose_name='Chirurgies Femmes')),
                ('refusal_male', models.PositiveIntegerField(verbose_name='Refus Hommes')),
                ('refusal_female', models.PositiveIntegerField(verbose_name='Refus Femmes')),
                ('recidivism_male', models.PositiveIntegerField(verbose_name='R\xe9cidives Hommes')),
                ('recidivism_female', models.PositiveIntegerField(verbose_name='R\xe9cidives Femmes')),
                ('community_assistance', models.BooleanField(default=False, verbose_name='Assistance relais')),
                ('nb_village_reports', models.PositiveIntegerField()),
                ('nb_community_assistance', models.PositiveIntegerField()),
                ('nb_days_min', models.PositiveIntegerField()),
                ('nb_days_max', models.PositiveIntegerField()),
                ('nb_days_avg', models.FloatField()),
                ('nb_days_med', models.FloatField()),
                ('nb_days_total', models.PositiveIntegerField()),
                ('agg_sources', models.ManyToManyField(related_name='aggregated_agg_aggttbacklogmissionr_reports', null=True, verbose_name='Aggr. Sources (all)', to='snisi_trachoma.AggTTBacklogMissionR', blank=True)),
                ('direct_agg_sources', models.ManyToManyField(related_name='direct_aggregated_agg_aggttbacklogmissionr_reports', null=True, verbose_name='Aggr. Sources (direct)', to='snisi_trachoma.AggTTBacklogMissionR', blank=True)),
            ],
            options={
                'verbose_name': 'Aggregated TT Backlog Mission Report',
                'verbose_name_plural': 'Aggregated TT Backlog Mission Reports',
            },
            bases=('snisi_core.snisireport', models.Model),
        ),
        migrations.CreateModel(
            name='TTBacklogMissionR',
            fields=[
                ('snisireport_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='snisi_core.SNISIReport')),
                ('started_on', models.DateField(verbose_name='Date de d\xe9marrage')),
                ('ended_on', models.DateField(null=True, verbose_name='Date de fin', blank=True)),
                ('operator_type', models.CharField(max_length=75, verbose_name='Profil op\xe9rateur', choices=[('OPT', 'OPT'), ('TSO', 'TSO'), ('AMO', 'AMO')])),
                ('strategy', models.CharField(max_length=75, verbose_name='Strat\xe9gie', choices=[('mobile', 'Mobile'), ('fixed', 'Fixed'), ('advanced', 'Advanced')])),
                ('consultation_male', models.PositiveIntegerField(default=0, verbose_name='Consultations Hommes')),
                ('consultation_female', models.PositiveIntegerField(default=0, verbose_name='Consultations Femmes')),
                ('surgery_male', models.PositiveIntegerField(default=0, verbose_name='Chirurgies Hommes')),
                ('surgery_female', models.PositiveIntegerField(default=0, verbose_name='Chirurgies Femmes')),
                ('refusal_male', models.PositiveIntegerField(default=0, verbose_name='Refus Hommes')),
                ('refusal_female', models.PositiveIntegerField(default=0, verbose_name='Refus Femmes')),
                ('recidivism_male', models.PositiveIntegerField(default=0, verbose_name='R\xe9cidives Hommes')),
                ('recidivism_female', models.PositiveIntegerField(default=0, verbose_name='R\xe9cidives Femmes')),
                ('community_assistance', models.BooleanField(default=0, verbose_name='Assistance relais')),
                ('nb_village_reports', models.PositiveIntegerField(default=0, verbose_name='Nb de villages visit\xe9s')),
                ('nb_community_assistance', models.PositiveIntegerField(default=0, verbose_name='Nb de village avec aide relais')),
                ('nb_days_min', models.PositiveIntegerField(default=0)),
                ('nb_days_max', models.PositiveIntegerField(default=0)),
                ('nb_days_mean', models.FloatField(default=0)),
                ('nb_days_median', models.FloatField(default=0)),
                ('nb_days_total', models.PositiveIntegerField(default=0)),
                ('operator', models.ForeignKey(verbose_name='Op\xe9rateur', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'TT Backlog Mission Report',
                'verbose_name_plural': 'TT Backlog Mission Reports',
            },
            bases=('snisi_core.snisireport',),
        ),
        migrations.CreateModel(
            name='TTBacklogVillageR',
            fields=[
                ('snisireport_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='snisi_core.SNISIReport')),
                ('consultation_male', models.PositiveIntegerField(verbose_name='Consultations Hommes')),
                ('consultation_female', models.PositiveIntegerField(verbose_name='Consultations Femmes')),
                ('surgery_male', models.PositiveIntegerField(verbose_name='Chirurgies Hommes')),
                ('surgery_female', models.PositiveIntegerField(verbose_name='Chirurgies Femmes')),
                ('refusal_male', models.PositiveIntegerField(verbose_name='Refus Hommes')),
                ('refusal_female', models.PositiveIntegerField(verbose_name='Refus Femmes')),
                ('recidivism_male', models.PositiveIntegerField(verbose_name='R\xe9cidives Hommes')),
                ('recidivism_female', models.PositiveIntegerField(verbose_name='R\xe9cidives Femmes')),
                ('community_assistance', models.BooleanField(default=False, verbose_name='Assistance relais')),
                ('arrived_on', models.DateField(verbose_name="Date d'arriv\xe9e")),
                ('left_on', models.DateField(verbose_name='Date de d\xe9part')),
                ('location', models.ForeignKey(to='snisi_core.Entity')),
            ],
            options={
                'verbose_name': 'TT Backlog Village Report',
                'verbose_name_plural': 'TT Backlog Village Reports',
            },
            bases=('snisi_core.snisireport',),
        ),
        migrations.AddField(
            model_name='ttbacklogmissionr',
            name='village_reports',
            field=models.ManyToManyField(to='snisi_trachoma.TTBacklogVillageR', null=True, verbose_name='Rapports Villages', blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='aggttbacklogmissionr',
            name='village_reports',
            field=models.ManyToManyField(to='snisi_trachoma.TTBacklogVillageR', null=True, verbose_name='Rapports Villages', blank=True),
            preserve_default=True,
        ),
    ]
