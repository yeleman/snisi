# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import snisi_malaria.models


class Migration(migrations.Migration):

    dependencies = [
        ('snisi_core', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='AggEpidemioMalariaR',
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
                ('u5_total_consultation_all_causes', models.PositiveIntegerField(default=0, verbose_name='Total Consultation All Causes')),
                ('u5_total_suspected_malaria_cases', models.PositiveIntegerField(default=0, verbose_name='Total Suspected Malaria Cases')),
                ('u5_total_rdt_tested_malaria_cases', models.PositiveIntegerField(default=0, verbose_name='Total RDT Tested Malaria Cases')),
                ('u5_total_rdt_confirmed_malaria_cases', models.PositiveIntegerField(default=0, verbose_name='Total RDT Confirmed Malaria Cases')),
                ('u5_total_rdt_pfalciparum_malaria_cases', models.PositiveIntegerField(default=0, verbose_name='Total RDT Confirmed P.Falciparum Malaria Cases')),
                ('u5_total_ts_tested_malaria_cases', models.PositiveIntegerField(default=0, verbose_name='Total TS Tested Malaria Cases')),
                ('u5_total_ts_confirmed_malaria_cases', models.PositiveIntegerField(default=0, verbose_name='Total TS Confirmed Malaria Cases')),
                ('u5_total_ts_pfalciparum_malaria_cases', models.PositiveIntegerField(default=0, verbose_name='Total TS Confirmed P.Falciparum Malaria Cases')),
                ('u5_total_simple_malaria_cases', models.PositiveIntegerField(default=0, verbose_name='Total Simple Malaria Cases')),
                ('u5_total_severe_malaria_cases', models.PositiveIntegerField(default=0, verbose_name='Total Severe Malaria Cases')),
                ('u5_total_death_all_causes', models.PositiveIntegerField(default=0, verbose_name='Total Death All Causes')),
                ('u5_total_malaria_death', models.PositiveIntegerField(default=0, verbose_name='Total Malaria Death')),
                ('o5_total_consultation_all_causes', models.PositiveIntegerField(default=0, verbose_name='Total Consultation All Causes')),
                ('o5_total_suspected_malaria_cases', models.PositiveIntegerField(default=0, verbose_name='Total Suspected Malaria Cases')),
                ('o5_total_rdt_tested_malaria_cases', models.PositiveIntegerField(default=0, verbose_name='Total RDT Tested Malaria Cases')),
                ('o5_total_rdt_confirmed_malaria_cases', models.PositiveIntegerField(default=0, verbose_name='Total RDT Confirmed Malaria Cases')),
                ('o5_total_rdt_pfalciparum_malaria_cases', models.PositiveIntegerField(default=0, verbose_name='Total RDT Confirmed P.Falciparum Malaria Cases')),
                ('o5_total_ts_tested_malaria_cases', models.PositiveIntegerField(default=0, verbose_name='Total TS Tested Malaria Cases')),
                ('o5_total_ts_confirmed_malaria_cases', models.PositiveIntegerField(default=0, verbose_name='Total TS Confirmed Malaria Cases')),
                ('o5_total_ts_pfalciparum_malaria_cases', models.PositiveIntegerField(default=0, verbose_name='Total TS Confirmed P.Falciparum Malaria Cases')),
                ('o5_total_simple_malaria_cases', models.PositiveIntegerField(default=0, verbose_name='Total Simple Malaria Cases')),
                ('o5_total_severe_malaria_cases', models.PositiveIntegerField(default=0, verbose_name='Total Severe Malaria Cases')),
                ('o5_total_death_all_causes', models.PositiveIntegerField(default=0, verbose_name='Total Death All Causes')),
                ('o5_total_malaria_death', models.PositiveIntegerField(default=0, verbose_name='Total Malaria Death')),
                ('pw_total_consultation_all_causes', models.PositiveIntegerField(default=0, verbose_name='Total Consultation All Causes')),
                ('pw_total_suspected_malaria_cases', models.PositiveIntegerField(default=0, verbose_name='Total Suspected Malaria Cases')),
                ('pw_total_rdt_tested_malaria_cases', models.PositiveIntegerField(default=0, verbose_name='Total RDT Tested Malaria Cases')),
                ('pw_total_rdt_confirmed_malaria_cases', models.PositiveIntegerField(default=0, verbose_name='Total RDT Confirmed Malaria Cases')),
                ('pw_total_rdt_pfalciparum_malaria_cases', models.PositiveIntegerField(default=0, verbose_name='Total RDT Confirmed P.Falciparum Malaria Cases')),
                ('pw_total_ts_tested_malaria_cases', models.PositiveIntegerField(default=0, verbose_name='Total TS Tested Malaria Cases')),
                ('pw_total_ts_confirmed_malaria_cases', models.PositiveIntegerField(default=0, verbose_name='Total TS Confirmed Malaria Cases')),
                ('pw_total_ts_pfalciparum_malaria_cases', models.PositiveIntegerField(default=0, verbose_name='Total TS Confirmed P.Falciparum Malaria Cases')),
                ('pw_total_simple_malaria_cases', models.PositiveIntegerField(default=0, verbose_name='Total Simple Malaria Cases')),
                ('pw_total_severe_malaria_cases', models.PositiveIntegerField(default=0, verbose_name='Total Severe Malaria Cases')),
                ('pw_total_death_all_causes', models.PositiveIntegerField(default=0, verbose_name='Total Death All Causes')),
                ('pw_total_malaria_death', models.PositiveIntegerField(default=0, verbose_name='Total Malaria Death')),
                ('agg_sources', models.ManyToManyField(related_name='aggregated_agg_aggepidemiomalariar_reports', null=True, verbose_name='Aggr. Sources (all)', to='snisi_malaria.AggEpidemioMalariaR', blank=True)),
                ('direct_agg_sources', models.ManyToManyField(related_name='direct_aggregated_agg_aggepidemiomalariar_reports', null=True, verbose_name='Aggr. Sources (direct)', to='snisi_malaria.AggEpidemioMalariaR', blank=True)),
            ],
            options={
                'verbose_name': 'Aggregated Epidemiology Malaria Report',
                'verbose_name_plural': 'Aggregated Epidemology Malaria Reports',
            },
            bases=('snisi_core.snisireport', models.Model),
        ),
        migrations.CreateModel(
            name='AggMalariaR',
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
                ('u5_total_consultation_all_causes', models.PositiveIntegerField(verbose_name='Total Consultation All Causes')),
                ('u5_total_suspected_malaria_cases', models.PositiveIntegerField(verbose_name='Total Suspected Malaria Cases')),
                ('u5_total_simple_malaria_cases', models.PositiveIntegerField(verbose_name='Total Simple Malaria Cases')),
                ('u5_total_severe_malaria_cases', models.PositiveIntegerField(verbose_name='Total Severe Malaria Cases')),
                ('u5_total_tested_malaria_cases', models.PositiveIntegerField(verbose_name='Total Tested Malaria Cases')),
                ('u5_total_confirmed_malaria_cases', models.PositiveIntegerField(verbose_name='Total Confirmed Malaria Cases')),
                ('u5_total_treated_malaria_cases', models.PositiveIntegerField(verbose_name='Total Treated Malaria Cases')),
                ('u5_total_inpatient_all_causes', models.PositiveIntegerField(verbose_name='Total Inpatient All Causes')),
                ('u5_total_malaria_inpatient', models.PositiveIntegerField(verbose_name='Total Malaria Inpatient')),
                ('u5_total_death_all_causes', models.PositiveIntegerField(verbose_name='Total Death All Causes')),
                ('u5_total_malaria_death', models.PositiveIntegerField(verbose_name='Total Malaria Death')),
                ('u5_total_distributed_bednets', models.PositiveIntegerField(verbose_name='Total Distributed Bednets')),
                ('o5_total_consultation_all_causes', models.PositiveIntegerField(verbose_name='Total Consultation All Causes')),
                ('o5_total_suspected_malaria_cases', models.PositiveIntegerField(verbose_name='Total Suspected Malaria Cases')),
                ('o5_total_simple_malaria_cases', models.PositiveIntegerField(verbose_name='Total Simple Malaria Cases')),
                ('o5_total_severe_malaria_cases', models.PositiveIntegerField(verbose_name='Total Severe Malaria Cases')),
                ('o5_total_tested_malaria_cases', models.PositiveIntegerField(verbose_name='Total Tested Malaria Cases')),
                ('o5_total_confirmed_malaria_cases', models.PositiveIntegerField(verbose_name='Total Confirmed Malaria Cases')),
                ('o5_total_treated_malaria_cases', models.PositiveIntegerField(verbose_name='Total Treated Malaria Cases')),
                ('o5_total_inpatient_all_causes', models.PositiveIntegerField(verbose_name='Total Inpatient All Causes')),
                ('o5_total_malaria_inpatient', models.PositiveIntegerField(verbose_name='Total Malaria Inpatient')),
                ('o5_total_death_all_causes', models.PositiveIntegerField(verbose_name='Total Death All Causes')),
                ('o5_total_malaria_death', models.PositiveIntegerField(verbose_name='Total Malaria Death')),
                ('pw_total_consultation_all_causes', models.PositiveIntegerField(verbose_name='Total Consultation All Causes')),
                ('pw_total_suspected_malaria_cases', models.PositiveIntegerField(verbose_name='Total Suspected Malaria Cases')),
                ('pw_total_severe_malaria_cases', models.PositiveIntegerField(verbose_name='Total Severe Malaria Cases')),
                ('pw_total_tested_malaria_cases', models.PositiveIntegerField(verbose_name='Total Tested Malaria Cases')),
                ('pw_total_confirmed_malaria_cases', models.PositiveIntegerField(verbose_name='Total Confirmed Malaria Cases')),
                ('pw_total_treated_malaria_cases', models.PositiveIntegerField(verbose_name='Total Treated Malaria Cases')),
                ('pw_total_inpatient_all_causes', models.PositiveIntegerField(verbose_name='Total Inpatient All Causes')),
                ('pw_total_malaria_inpatient', models.PositiveIntegerField(verbose_name='Total Malaria Inpatient')),
                ('pw_total_death_all_causes', models.PositiveIntegerField(verbose_name='Total Death All Causes')),
                ('pw_total_malaria_death', models.PositiveIntegerField(verbose_name='Total Malaria Death')),
                ('pw_total_distributed_bednets', models.PositiveIntegerField(verbose_name='Total Distributed Bednets')),
                ('pw_total_anc1', models.PositiveIntegerField(verbose_name='Total ANC1 Visits')),
                ('pw_total_sp1', models.PositiveIntegerField(verbose_name='Total SP1 given')),
                ('pw_total_sp2', models.PositiveIntegerField(verbose_name='Total SP2 given')),
                ('stockout_act_children', models.PositiveIntegerField(verbose_name='ACT Children')),
                ('stockout_act_youth', models.PositiveIntegerField(verbose_name='ACT Youth')),
                ('stockout_act_adult', models.PositiveIntegerField(verbose_name='ACT Adult')),
                ('stockout_artemether', models.PositiveIntegerField(verbose_name='Artemether')),
                ('stockout_quinine', models.PositiveIntegerField(verbose_name='Quinine')),
                ('stockout_serum', models.PositiveIntegerField(verbose_name='Serum')),
                ('stockout_bednet', models.PositiveIntegerField(verbose_name='Bednets')),
                ('stockout_rdt', models.PositiveIntegerField(verbose_name='RDTs')),
                ('stockout_sp', models.PositiveIntegerField(verbose_name='SPs')),
                ('agg_sources', models.ManyToManyField(related_name='aggregated_agg_aggmalariar_reports', null=True, verbose_name='Aggr. Sources (all)', to='snisi_malaria.AggMalariaR', blank=True)),
                ('direct_agg_sources', models.ManyToManyField(related_name='direct_aggregated_agg_aggmalariar_reports', null=True, verbose_name='Aggr. Sources (direct)', to='snisi_malaria.AggMalariaR', blank=True)),
            ],
            options={
                'verbose_name': 'Aggregated Malaria Report',
                'verbose_name_plural': 'Aggregated Malaria Reports',
            },
            bases=(snisi_malaria.models.MalariaRIface, 'snisi_core.snisireport', models.Model),
        ),
        migrations.CreateModel(
            name='EpidemioMalariaR',
            fields=[
                ('snisireport_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='snisi_core.SNISIReport')),
                ('u5_total_consultation_all_causes', models.PositiveIntegerField(default=0, verbose_name='Total Consultation All Causes')),
                ('u5_total_suspected_malaria_cases', models.PositiveIntegerField(default=0, verbose_name='Total Suspected Malaria Cases')),
                ('u5_total_rdt_tested_malaria_cases', models.PositiveIntegerField(default=0, verbose_name='Total RDT Tested Malaria Cases')),
                ('u5_total_rdt_confirmed_malaria_cases', models.PositiveIntegerField(default=0, verbose_name='Total RDT Confirmed Malaria Cases')),
                ('u5_total_rdt_pfalciparum_malaria_cases', models.PositiveIntegerField(default=0, verbose_name='Total RDT Confirmed P.Falciparum Malaria Cases')),
                ('u5_total_ts_tested_malaria_cases', models.PositiveIntegerField(default=0, verbose_name='Total TS Tested Malaria Cases')),
                ('u5_total_ts_confirmed_malaria_cases', models.PositiveIntegerField(default=0, verbose_name='Total TS Confirmed Malaria Cases')),
                ('u5_total_ts_pfalciparum_malaria_cases', models.PositiveIntegerField(default=0, verbose_name='Total TS Confirmed P.Falciparum Malaria Cases')),
                ('u5_total_simple_malaria_cases', models.PositiveIntegerField(default=0, verbose_name='Total Simple Malaria Cases')),
                ('u5_total_severe_malaria_cases', models.PositiveIntegerField(default=0, verbose_name='Total Severe Malaria Cases')),
                ('u5_total_death_all_causes', models.PositiveIntegerField(default=0, verbose_name='Total Death All Causes')),
                ('u5_total_malaria_death', models.PositiveIntegerField(default=0, verbose_name='Total Malaria Death')),
                ('o5_total_consultation_all_causes', models.PositiveIntegerField(default=0, verbose_name='Total Consultation All Causes')),
                ('o5_total_suspected_malaria_cases', models.PositiveIntegerField(default=0, verbose_name='Total Suspected Malaria Cases')),
                ('o5_total_rdt_tested_malaria_cases', models.PositiveIntegerField(default=0, verbose_name='Total RDT Tested Malaria Cases')),
                ('o5_total_rdt_confirmed_malaria_cases', models.PositiveIntegerField(default=0, verbose_name='Total RDT Confirmed Malaria Cases')),
                ('o5_total_rdt_pfalciparum_malaria_cases', models.PositiveIntegerField(default=0, verbose_name='Total RDT Confirmed P.Falciparum Malaria Cases')),
                ('o5_total_ts_tested_malaria_cases', models.PositiveIntegerField(default=0, verbose_name='Total TS Tested Malaria Cases')),
                ('o5_total_ts_confirmed_malaria_cases', models.PositiveIntegerField(default=0, verbose_name='Total TS Confirmed Malaria Cases')),
                ('o5_total_ts_pfalciparum_malaria_cases', models.PositiveIntegerField(default=0, verbose_name='Total TS Confirmed P.Falciparum Malaria Cases')),
                ('o5_total_simple_malaria_cases', models.PositiveIntegerField(default=0, verbose_name='Total Simple Malaria Cases')),
                ('o5_total_severe_malaria_cases', models.PositiveIntegerField(default=0, verbose_name='Total Severe Malaria Cases')),
                ('o5_total_death_all_causes', models.PositiveIntegerField(default=0, verbose_name='Total Death All Causes')),
                ('o5_total_malaria_death', models.PositiveIntegerField(default=0, verbose_name='Total Malaria Death')),
                ('pw_total_consultation_all_causes', models.PositiveIntegerField(default=0, verbose_name='Total Consultation All Causes')),
                ('pw_total_suspected_malaria_cases', models.PositiveIntegerField(default=0, verbose_name='Total Suspected Malaria Cases')),
                ('pw_total_rdt_tested_malaria_cases', models.PositiveIntegerField(default=0, verbose_name='Total RDT Tested Malaria Cases')),
                ('pw_total_rdt_confirmed_malaria_cases', models.PositiveIntegerField(default=0, verbose_name='Total RDT Confirmed Malaria Cases')),
                ('pw_total_rdt_pfalciparum_malaria_cases', models.PositiveIntegerField(default=0, verbose_name='Total RDT Confirmed P.Falciparum Malaria Cases')),
                ('pw_total_ts_tested_malaria_cases', models.PositiveIntegerField(default=0, verbose_name='Total TS Tested Malaria Cases')),
                ('pw_total_ts_confirmed_malaria_cases', models.PositiveIntegerField(default=0, verbose_name='Total TS Confirmed Malaria Cases')),
                ('pw_total_ts_pfalciparum_malaria_cases', models.PositiveIntegerField(default=0, verbose_name='Total TS Confirmed P.Falciparum Malaria Cases')),
                ('pw_total_simple_malaria_cases', models.PositiveIntegerField(default=0, verbose_name='Total Simple Malaria Cases')),
                ('pw_total_severe_malaria_cases', models.PositiveIntegerField(default=0, verbose_name='Total Severe Malaria Cases')),
                ('pw_total_death_all_causes', models.PositiveIntegerField(default=0, verbose_name='Total Death All Causes')),
                ('pw_total_malaria_death', models.PositiveIntegerField(default=0, verbose_name='Total Malaria Death')),
            ],
            options={
                'verbose_name': 'Epidemiology Malaria Report',
                'verbose_name_plural': 'Epidemology Malaria Reports',
            },
            bases=('snisi_core.snisireport', models.Model),
        ),
        migrations.CreateModel(
            name='MalariaR',
            fields=[
                ('snisireport_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='snisi_core.SNISIReport')),
                ('u5_total_consultation_all_causes', models.PositiveIntegerField(verbose_name='Total Consultation All Causes')),
                ('u5_total_suspected_malaria_cases', models.PositiveIntegerField(verbose_name='Total Suspected Malaria Cases')),
                ('u5_total_simple_malaria_cases', models.PositiveIntegerField(verbose_name='Total Simple Malaria Cases')),
                ('u5_total_severe_malaria_cases', models.PositiveIntegerField(verbose_name='Total Severe Malaria Cases')),
                ('u5_total_tested_malaria_cases', models.PositiveIntegerField(verbose_name='Total Tested Malaria Cases')),
                ('u5_total_confirmed_malaria_cases', models.PositiveIntegerField(verbose_name='Total Confirmed Malaria Cases')),
                ('u5_total_treated_malaria_cases', models.PositiveIntegerField(verbose_name='Total Treated Malaria Cases')),
                ('u5_total_inpatient_all_causes', models.PositiveIntegerField(verbose_name='Total Inpatient All Causes')),
                ('u5_total_malaria_inpatient', models.PositiveIntegerField(verbose_name='Total Malaria Inpatient')),
                ('u5_total_death_all_causes', models.PositiveIntegerField(verbose_name='Total Death All Causes')),
                ('u5_total_malaria_death', models.PositiveIntegerField(verbose_name='Total Malaria Death')),
                ('u5_total_distributed_bednets', models.PositiveIntegerField(verbose_name='Total Distributed Bednets')),
                ('o5_total_consultation_all_causes', models.PositiveIntegerField(verbose_name='Total Consultation All Causes')),
                ('o5_total_suspected_malaria_cases', models.PositiveIntegerField(verbose_name='Total Suspected Malaria Cases')),
                ('o5_total_simple_malaria_cases', models.PositiveIntegerField(verbose_name='Total Simple Malaria Cases')),
                ('o5_total_severe_malaria_cases', models.PositiveIntegerField(verbose_name='Total Severe Malaria Cases')),
                ('o5_total_tested_malaria_cases', models.PositiveIntegerField(verbose_name='Total Tested Malaria Cases')),
                ('o5_total_confirmed_malaria_cases', models.PositiveIntegerField(verbose_name='Total Confirmed Malaria Cases')),
                ('o5_total_treated_malaria_cases', models.PositiveIntegerField(verbose_name='Total Treated Malaria Cases')),
                ('o5_total_inpatient_all_causes', models.PositiveIntegerField(verbose_name='Total Inpatient All Causes')),
                ('o5_total_malaria_inpatient', models.PositiveIntegerField(verbose_name='Total Malaria Inpatient')),
                ('o5_total_death_all_causes', models.PositiveIntegerField(verbose_name='Total Death All Causes')),
                ('o5_total_malaria_death', models.PositiveIntegerField(verbose_name='Total Malaria Death')),
                ('pw_total_consultation_all_causes', models.PositiveIntegerField(verbose_name='Total Consultation All Causes')),
                ('pw_total_suspected_malaria_cases', models.PositiveIntegerField(verbose_name='Total Suspected Malaria Cases')),
                ('pw_total_severe_malaria_cases', models.PositiveIntegerField(verbose_name='Total Severe Malaria Cases')),
                ('pw_total_tested_malaria_cases', models.PositiveIntegerField(verbose_name='Total Tested Malaria Cases')),
                ('pw_total_confirmed_malaria_cases', models.PositiveIntegerField(verbose_name='Total Confirmed Malaria Cases')),
                ('pw_total_treated_malaria_cases', models.PositiveIntegerField(verbose_name='Total Treated Malaria Cases')),
                ('pw_total_inpatient_all_causes', models.PositiveIntegerField(verbose_name='Total Inpatient All Causes')),
                ('pw_total_malaria_inpatient', models.PositiveIntegerField(verbose_name='Total Malaria Inpatient')),
                ('pw_total_death_all_causes', models.PositiveIntegerField(verbose_name='Total Death All Causes')),
                ('pw_total_malaria_death', models.PositiveIntegerField(verbose_name='Total Malaria Death')),
                ('pw_total_distributed_bednets', models.PositiveIntegerField(verbose_name='Total Distributed Bednets')),
                ('pw_total_anc1', models.PositiveIntegerField(verbose_name='Total ANC1 Visits')),
                ('pw_total_sp1', models.PositiveIntegerField(verbose_name='Total SP1 given')),
                ('pw_total_sp2', models.PositiveIntegerField(verbose_name='Total SP2 given')),
                ('stockout_act_children', models.CharField(max_length=1, verbose_name='ACT Children', choices=[('Y', 'Yes'), ('N', 'No')])),
                ('stockout_act_youth', models.CharField(max_length=1, verbose_name='ACT Youth', choices=[('Y', 'Yes'), ('N', 'No')])),
                ('stockout_act_adult', models.CharField(max_length=1, verbose_name='ACT Adult', choices=[('Y', 'Yes'), ('N', 'No')])),
                ('stockout_artemether', models.CharField(max_length=1, verbose_name='Artemether', choices=[('Y', 'Yes'), ('N', 'No')])),
                ('stockout_quinine', models.CharField(max_length=1, verbose_name='Quinine', choices=[('Y', 'Yes'), ('N', 'No')])),
                ('stockout_serum', models.CharField(max_length=1, verbose_name='Serum', choices=[('Y', 'Yes'), ('N', 'No')])),
                ('stockout_bednet', models.CharField(max_length=1, verbose_name='Bednets', choices=[('Y', 'Yes'), ('N', 'No')])),
                ('stockout_rdt', models.CharField(max_length=1, verbose_name='RDTs', choices=[('Y', 'Yes'), ('N', 'No')])),
                ('stockout_sp', models.CharField(max_length=1, verbose_name='SPs', choices=[('Y', 'Yes'), ('N', 'No')])),
            ],
            options={
                'verbose_name': 'Malaria Report',
                'verbose_name_plural': 'Malaria Reports',
            },
            bases=(snisi_malaria.models.MalariaRIface, 'snisi_core.snisireport'),
        ),
        migrations.AddField(
            model_name='aggmalariar',
            name='direct_indiv_sources',
            field=models.ManyToManyField(related_name='direct_source_agg_aggmalariar_reports', null=True, verbose_name='Primary. Sources (direct)', to='snisi_malaria.MalariaR', blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='aggmalariar',
            name='indiv_sources',
            field=models.ManyToManyField(related_name='source_agg_aggmalariar_reports', null=True, verbose_name='Primary. Sources (all)', to='snisi_malaria.MalariaR', blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='aggepidemiomalariar',
            name='direct_indiv_sources',
            field=models.ManyToManyField(related_name='direct_source_agg_aggepidemiomalariar_reports', null=True, verbose_name='Primary. Sources (direct)', to='snisi_malaria.EpidemioMalariaR', blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='aggepidemiomalariar',
            name='indiv_sources',
            field=models.ManyToManyField(related_name='source_agg_aggepidemiomalariar_reports', null=True, verbose_name='Primary. Sources (all)', to='snisi_malaria.EpidemioMalariaR', blank=True),
            preserve_default=True,
        ),
    ]
