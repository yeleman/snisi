# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'MalariaR'
        db.create_table(u'snisi_malaria_malariar', (
            (u'snisireport_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['snisi_core.SNISIReport'], unique=True, primary_key=True)),
            ('u5_total_consultation_all_causes', self.gf('django.db.models.fields.PositiveIntegerField')()),
            ('u5_total_suspected_malaria_cases', self.gf('django.db.models.fields.PositiveIntegerField')()),
            ('u5_total_simple_malaria_cases', self.gf('django.db.models.fields.PositiveIntegerField')()),
            ('u5_total_severe_malaria_cases', self.gf('django.db.models.fields.PositiveIntegerField')()),
            ('u5_total_tested_malaria_cases', self.gf('django.db.models.fields.PositiveIntegerField')()),
            ('u5_total_confirmed_malaria_cases', self.gf('django.db.models.fields.PositiveIntegerField')()),
            ('u5_total_treated_malaria_cases', self.gf('django.db.models.fields.PositiveIntegerField')()),
            ('u5_total_inpatient_all_causes', self.gf('django.db.models.fields.PositiveIntegerField')()),
            ('u5_total_malaria_inpatient', self.gf('django.db.models.fields.PositiveIntegerField')()),
            ('u5_total_death_all_causes', self.gf('django.db.models.fields.PositiveIntegerField')()),
            ('u5_total_malaria_death', self.gf('django.db.models.fields.PositiveIntegerField')()),
            ('u5_total_distributed_bednets', self.gf('django.db.models.fields.PositiveIntegerField')()),
            ('o5_total_consultation_all_causes', self.gf('django.db.models.fields.PositiveIntegerField')()),
            ('o5_total_suspected_malaria_cases', self.gf('django.db.models.fields.PositiveIntegerField')()),
            ('o5_total_simple_malaria_cases', self.gf('django.db.models.fields.PositiveIntegerField')()),
            ('o5_total_severe_malaria_cases', self.gf('django.db.models.fields.PositiveIntegerField')()),
            ('o5_total_tested_malaria_cases', self.gf('django.db.models.fields.PositiveIntegerField')()),
            ('o5_total_confirmed_malaria_cases', self.gf('django.db.models.fields.PositiveIntegerField')()),
            ('o5_total_treated_malaria_cases', self.gf('django.db.models.fields.PositiveIntegerField')()),
            ('o5_total_inpatient_all_causes', self.gf('django.db.models.fields.PositiveIntegerField')()),
            ('o5_total_malaria_inpatient', self.gf('django.db.models.fields.PositiveIntegerField')()),
            ('o5_total_death_all_causes', self.gf('django.db.models.fields.PositiveIntegerField')()),
            ('o5_total_malaria_death', self.gf('django.db.models.fields.PositiveIntegerField')()),
            ('pw_total_consultation_all_causes', self.gf('django.db.models.fields.PositiveIntegerField')()),
            ('pw_total_suspected_malaria_cases', self.gf('django.db.models.fields.PositiveIntegerField')()),
            ('pw_total_severe_malaria_cases', self.gf('django.db.models.fields.PositiveIntegerField')()),
            ('pw_total_tested_malaria_cases', self.gf('django.db.models.fields.PositiveIntegerField')()),
            ('pw_total_confirmed_malaria_cases', self.gf('django.db.models.fields.PositiveIntegerField')()),
            ('pw_total_treated_malaria_cases', self.gf('django.db.models.fields.PositiveIntegerField')()),
            ('pw_total_inpatient_all_causes', self.gf('django.db.models.fields.PositiveIntegerField')()),
            ('pw_total_malaria_inpatient', self.gf('django.db.models.fields.PositiveIntegerField')()),
            ('pw_total_death_all_causes', self.gf('django.db.models.fields.PositiveIntegerField')()),
            ('pw_total_malaria_death', self.gf('django.db.models.fields.PositiveIntegerField')()),
            ('pw_total_distributed_bednets', self.gf('django.db.models.fields.PositiveIntegerField')()),
            ('pw_total_anc1', self.gf('django.db.models.fields.PositiveIntegerField')()),
            ('pw_total_sp1', self.gf('django.db.models.fields.PositiveIntegerField')()),
            ('pw_total_sp2', self.gf('django.db.models.fields.PositiveIntegerField')()),
            ('stockout_act_children', self.gf('django.db.models.fields.CharField')(max_length=1)),
            ('stockout_act_youth', self.gf('django.db.models.fields.CharField')(max_length=1)),
            ('stockout_act_adult', self.gf('django.db.models.fields.CharField')(max_length=1)),
            ('stockout_artemether', self.gf('django.db.models.fields.CharField')(max_length=1)),
            ('stockout_quinine', self.gf('django.db.models.fields.CharField')(max_length=1)),
            ('stockout_serum', self.gf('django.db.models.fields.CharField')(max_length=1)),
            ('stockout_bednet', self.gf('django.db.models.fields.CharField')(max_length=1)),
            ('stockout_rdt', self.gf('django.db.models.fields.CharField')(max_length=1)),
            ('stockout_sp', self.gf('django.db.models.fields.CharField')(max_length=1)),
        ))
        db.send_create_signal(u'snisi_malaria', ['MalariaR'])

        # Adding model 'AggMalariaR'
        db.create_table(u'snisi_malaria_aggmalariar', (
            (u'snisireport_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['snisi_core.SNISIReport'], unique=True, primary_key=True)),
            ('nb_source_reports_expected', self.gf('django.db.models.fields.PositiveIntegerField')(null=True, blank=True)),
            ('nb_source_reports_arrived', self.gf('django.db.models.fields.PositiveIntegerField')(null=True, blank=True)),
            ('nb_source_reports_arrived_on_time', self.gf('django.db.models.fields.PositiveIntegerField')(null=True, blank=True)),
            ('nb_source_reports_arrived_correct', self.gf('django.db.models.fields.PositiveIntegerField')(null=True, blank=True)),
            ('nb_source_reports_arrived_complete', self.gf('django.db.models.fields.PositiveIntegerField')(null=True, blank=True)),
            ('nb_source_reports_altered', self.gf('django.db.models.fields.PositiveIntegerField')(null=True, blank=True)),
            ('nb_source_reports_validated', self.gf('django.db.models.fields.PositiveIntegerField')(null=True, blank=True)),
            ('nb_source_reports_auto_validated', self.gf('django.db.models.fields.PositiveIntegerField')(null=True, blank=True)),
            ('nb_agg_reports_altered', self.gf('django.db.models.fields.PositiveIntegerField')(null=True, blank=True)),
            ('nb_agg_reports_validated', self.gf('django.db.models.fields.PositiveIntegerField')(null=True, blank=True)),
            ('nb_agg_reports_auto_validated', self.gf('django.db.models.fields.PositiveIntegerField')(null=True, blank=True)),
            ('u5_total_consultation_all_causes', self.gf('django.db.models.fields.PositiveIntegerField')()),
            ('u5_total_suspected_malaria_cases', self.gf('django.db.models.fields.PositiveIntegerField')()),
            ('u5_total_simple_malaria_cases', self.gf('django.db.models.fields.PositiveIntegerField')()),
            ('u5_total_severe_malaria_cases', self.gf('django.db.models.fields.PositiveIntegerField')()),
            ('u5_total_tested_malaria_cases', self.gf('django.db.models.fields.PositiveIntegerField')()),
            ('u5_total_confirmed_malaria_cases', self.gf('django.db.models.fields.PositiveIntegerField')()),
            ('u5_total_treated_malaria_cases', self.gf('django.db.models.fields.PositiveIntegerField')()),
            ('u5_total_inpatient_all_causes', self.gf('django.db.models.fields.PositiveIntegerField')()),
            ('u5_total_malaria_inpatient', self.gf('django.db.models.fields.PositiveIntegerField')()),
            ('u5_total_death_all_causes', self.gf('django.db.models.fields.PositiveIntegerField')()),
            ('u5_total_malaria_death', self.gf('django.db.models.fields.PositiveIntegerField')()),
            ('u5_total_distributed_bednets', self.gf('django.db.models.fields.PositiveIntegerField')()),
            ('o5_total_consultation_all_causes', self.gf('django.db.models.fields.PositiveIntegerField')()),
            ('o5_total_suspected_malaria_cases', self.gf('django.db.models.fields.PositiveIntegerField')()),
            ('o5_total_simple_malaria_cases', self.gf('django.db.models.fields.PositiveIntegerField')()),
            ('o5_total_severe_malaria_cases', self.gf('django.db.models.fields.PositiveIntegerField')()),
            ('o5_total_tested_malaria_cases', self.gf('django.db.models.fields.PositiveIntegerField')()),
            ('o5_total_confirmed_malaria_cases', self.gf('django.db.models.fields.PositiveIntegerField')()),
            ('o5_total_treated_malaria_cases', self.gf('django.db.models.fields.PositiveIntegerField')()),
            ('o5_total_inpatient_all_causes', self.gf('django.db.models.fields.PositiveIntegerField')()),
            ('o5_total_malaria_inpatient', self.gf('django.db.models.fields.PositiveIntegerField')()),
            ('o5_total_death_all_causes', self.gf('django.db.models.fields.PositiveIntegerField')()),
            ('o5_total_malaria_death', self.gf('django.db.models.fields.PositiveIntegerField')()),
            ('pw_total_consultation_all_causes', self.gf('django.db.models.fields.PositiveIntegerField')()),
            ('pw_total_suspected_malaria_cases', self.gf('django.db.models.fields.PositiveIntegerField')()),
            ('pw_total_severe_malaria_cases', self.gf('django.db.models.fields.PositiveIntegerField')()),
            ('pw_total_tested_malaria_cases', self.gf('django.db.models.fields.PositiveIntegerField')()),
            ('pw_total_confirmed_malaria_cases', self.gf('django.db.models.fields.PositiveIntegerField')()),
            ('pw_total_treated_malaria_cases', self.gf('django.db.models.fields.PositiveIntegerField')()),
            ('pw_total_inpatient_all_causes', self.gf('django.db.models.fields.PositiveIntegerField')()),
            ('pw_total_malaria_inpatient', self.gf('django.db.models.fields.PositiveIntegerField')()),
            ('pw_total_death_all_causes', self.gf('django.db.models.fields.PositiveIntegerField')()),
            ('pw_total_malaria_death', self.gf('django.db.models.fields.PositiveIntegerField')()),
            ('pw_total_distributed_bednets', self.gf('django.db.models.fields.PositiveIntegerField')()),
            ('pw_total_anc1', self.gf('django.db.models.fields.PositiveIntegerField')()),
            ('pw_total_sp1', self.gf('django.db.models.fields.PositiveIntegerField')()),
            ('pw_total_sp2', self.gf('django.db.models.fields.PositiveIntegerField')()),
            ('stockout_act_children', self.gf('django.db.models.fields.PositiveIntegerField')()),
            ('stockout_act_youth', self.gf('django.db.models.fields.PositiveIntegerField')()),
            ('stockout_act_adult', self.gf('django.db.models.fields.PositiveIntegerField')()),
            ('stockout_artemether', self.gf('django.db.models.fields.PositiveIntegerField')()),
            ('stockout_quinine', self.gf('django.db.models.fields.PositiveIntegerField')()),
            ('stockout_serum', self.gf('django.db.models.fields.PositiveIntegerField')()),
            ('stockout_bednet', self.gf('django.db.models.fields.PositiveIntegerField')()),
            ('stockout_rdt', self.gf('django.db.models.fields.PositiveIntegerField')()),
            ('stockout_sp', self.gf('django.db.models.fields.PositiveIntegerField')()),
        ))
        db.send_create_signal(u'snisi_malaria', ['AggMalariaR'])

        # Adding M2M table for field agg_sources on 'AggMalariaR'
        m2m_table_name = db.shorten_name(u'snisi_malaria_aggmalariar_agg_sources')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('from_aggmalariar', models.ForeignKey(orm[u'snisi_malaria.aggmalariar'], null=False)),
            ('to_aggmalariar', models.ForeignKey(orm[u'snisi_malaria.aggmalariar'], null=False))
        ))
        db.create_unique(m2m_table_name, ['from_aggmalariar_id', 'to_aggmalariar_id'])

        # Adding M2M table for field direct_agg_sources on 'AggMalariaR'
        m2m_table_name = db.shorten_name(u'snisi_malaria_aggmalariar_direct_agg_sources')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('from_aggmalariar', models.ForeignKey(orm[u'snisi_malaria.aggmalariar'], null=False)),
            ('to_aggmalariar', models.ForeignKey(orm[u'snisi_malaria.aggmalariar'], null=False))
        ))
        db.create_unique(m2m_table_name, ['from_aggmalariar_id', 'to_aggmalariar_id'])

        # Adding M2M table for field indiv_sources on 'AggMalariaR'
        m2m_table_name = db.shorten_name(u'snisi_malaria_aggmalariar_indiv_sources')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('aggmalariar', models.ForeignKey(orm[u'snisi_malaria.aggmalariar'], null=False)),
            ('malariar', models.ForeignKey(orm[u'snisi_malaria.malariar'], null=False))
        ))
        db.create_unique(m2m_table_name, ['aggmalariar_id', 'malariar_id'])

        # Adding M2M table for field direct_indiv_sources on 'AggMalariaR'
        m2m_table_name = db.shorten_name(u'snisi_malaria_aggmalariar_direct_indiv_sources')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('aggmalariar', models.ForeignKey(orm[u'snisi_malaria.aggmalariar'], null=False)),
            ('malariar', models.ForeignKey(orm[u'snisi_malaria.malariar'], null=False))
        ))
        db.create_unique(m2m_table_name, ['aggmalariar_id', 'malariar_id'])

        # Adding model 'EpidemioMalariaR'
        db.create_table(u'snisi_malaria_epidemiomalariar', (
            (u'snisireport_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['snisi_core.SNISIReport'], unique=True, primary_key=True)),
            ('u5_total_consultation_all_causes', self.gf('django.db.models.fields.PositiveIntegerField')()),
            ('u5_total_suspected_malaria_cases', self.gf('django.db.models.fields.PositiveIntegerField')()),
            ('u5_total_tdr_tested_malaria_cases', self.gf('django.db.models.fields.PositiveIntegerField')()),
            ('u5_total_tdr_confirmed_malaria_cases', self.gf('django.db.models.fields.PositiveIntegerField')()),
            ('u5_total_tdr_parasite_pf_malaria_cases', self.gf('django.db.models.fields.PositiveIntegerField')()),
            ('u5_total_ge_tested_malaria_cases', self.gf('django.db.models.fields.PositiveIntegerField')()),
            ('u5_total_ge_confirmed_malaria_cases', self.gf('django.db.models.fields.PositiveIntegerField')()),
            ('u5_total_ge_parasite_pf_malaria_cases', self.gf('django.db.models.fields.PositiveIntegerField')()),
            ('u5_total_simple_malaria_cases', self.gf('django.db.models.fields.PositiveIntegerField')()),
            ('u5_total_severe_malaria_cases', self.gf('django.db.models.fields.PositiveIntegerField')()),
            ('u5_total_malaria_death', self.gf('django.db.models.fields.PositiveIntegerField')()),
            ('u5_total_death_all_causes', self.gf('django.db.models.fields.PositiveIntegerField')()),
            ('o5_total_consultation_all_causes', self.gf('django.db.models.fields.PositiveIntegerField')()),
            ('o5_total_suspected_malaria_cases', self.gf('django.db.models.fields.PositiveIntegerField')()),
            ('o5_total_tdr_tested_malaria_cases', self.gf('django.db.models.fields.PositiveIntegerField')()),
            ('o5_total_tdr_confirmed_malaria_cases', self.gf('django.db.models.fields.PositiveIntegerField')()),
            ('o5_total_tdr_parasite_pf_malaria_cases', self.gf('django.db.models.fields.PositiveIntegerField')()),
            ('o5_total_ge_tested_malaria_cases', self.gf('django.db.models.fields.PositiveIntegerField')()),
            ('o5_total_ge_confirmed_malaria_cases', self.gf('django.db.models.fields.PositiveIntegerField')()),
            ('o5_total_ge_parasite_pf_malaria_cases', self.gf('django.db.models.fields.PositiveIntegerField')()),
            ('o5_total_simple_malaria_cases', self.gf('django.db.models.fields.PositiveIntegerField')()),
            ('o5_total_severe_malaria_cases', self.gf('django.db.models.fields.PositiveIntegerField')()),
            ('o5_total_malaria_death', self.gf('django.db.models.fields.PositiveIntegerField')()),
            ('o5_total_death_all_causes', self.gf('django.db.models.fields.PositiveIntegerField')()),
            ('pw_total_consultation_all_causes', self.gf('django.db.models.fields.PositiveIntegerField')()),
            ('pw_total_suspected_malaria_cases', self.gf('django.db.models.fields.PositiveIntegerField')()),
            ('pw_total_tdr_tested_malaria_cases', self.gf('django.db.models.fields.PositiveIntegerField')()),
            ('pw_total_tdr_confirmed_malaria_cases', self.gf('django.db.models.fields.PositiveIntegerField')()),
            ('pw_total_tdr_parasite_pf_malaria_cases', self.gf('django.db.models.fields.PositiveIntegerField')()),
            ('pw_total_ge_tested_malaria_cases', self.gf('django.db.models.fields.PositiveIntegerField')()),
            ('pw_total_ge_confirmed_malaria_cases', self.gf('django.db.models.fields.PositiveIntegerField')()),
            ('pw_total_ge_parasite_pf_malaria_cases', self.gf('django.db.models.fields.PositiveIntegerField')()),
            ('pw_total_simple_malaria_cases', self.gf('django.db.models.fields.PositiveIntegerField')()),
            ('pw_total_severe_malaria_cases', self.gf('django.db.models.fields.PositiveIntegerField')()),
            ('pw_total_malaria_death', self.gf('django.db.models.fields.PositiveIntegerField')()),
            ('pw_total_death_all_causes', self.gf('django.db.models.fields.PositiveIntegerField')()),
        ))
        db.send_create_signal(u'snisi_malaria', ['EpidemioMalariaR'])

        # Adding model 'AggEpidemioMalariaR'
        db.create_table(u'snisi_malaria_aggepidemiomalariar', (
            (u'snisireport_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['snisi_core.SNISIReport'], unique=True, primary_key=True)),
            ('nb_source_reports_expected', self.gf('django.db.models.fields.PositiveIntegerField')(null=True, blank=True)),
            ('nb_source_reports_arrived', self.gf('django.db.models.fields.PositiveIntegerField')(null=True, blank=True)),
            ('nb_source_reports_arrived_on_time', self.gf('django.db.models.fields.PositiveIntegerField')(null=True, blank=True)),
            ('nb_source_reports_arrived_correct', self.gf('django.db.models.fields.PositiveIntegerField')(null=True, blank=True)),
            ('nb_source_reports_arrived_complete', self.gf('django.db.models.fields.PositiveIntegerField')(null=True, blank=True)),
            ('nb_source_reports_altered', self.gf('django.db.models.fields.PositiveIntegerField')(null=True, blank=True)),
            ('nb_source_reports_validated', self.gf('django.db.models.fields.PositiveIntegerField')(null=True, blank=True)),
            ('nb_source_reports_auto_validated', self.gf('django.db.models.fields.PositiveIntegerField')(null=True, blank=True)),
            ('nb_agg_reports_altered', self.gf('django.db.models.fields.PositiveIntegerField')(null=True, blank=True)),
            ('nb_agg_reports_validated', self.gf('django.db.models.fields.PositiveIntegerField')(null=True, blank=True)),
            ('nb_agg_reports_auto_validated', self.gf('django.db.models.fields.PositiveIntegerField')(null=True, blank=True)),
            ('u5_total_consultation_all_causes', self.gf('django.db.models.fields.PositiveIntegerField')()),
            ('u5_total_suspected_malaria_cases', self.gf('django.db.models.fields.PositiveIntegerField')()),
            ('u5_total_tdr_tested_malaria_cases', self.gf('django.db.models.fields.PositiveIntegerField')()),
            ('u5_total_tdr_confirmed_malaria_cases', self.gf('django.db.models.fields.PositiveIntegerField')()),
            ('u5_total_tdr_parasite_pf_malaria_cases', self.gf('django.db.models.fields.PositiveIntegerField')()),
            ('u5_total_ge_tested_malaria_cases', self.gf('django.db.models.fields.PositiveIntegerField')()),
            ('u5_total_ge_confirmed_malaria_cases', self.gf('django.db.models.fields.PositiveIntegerField')()),
            ('u5_total_ge_parasite_pf_malaria_cases', self.gf('django.db.models.fields.PositiveIntegerField')()),
            ('u5_total_simple_malaria_cases', self.gf('django.db.models.fields.PositiveIntegerField')()),
            ('u5_total_severe_malaria_cases', self.gf('django.db.models.fields.PositiveIntegerField')()),
            ('u5_total_malaria_death', self.gf('django.db.models.fields.PositiveIntegerField')()),
            ('u5_total_death_all_causes', self.gf('django.db.models.fields.PositiveIntegerField')()),
            ('o5_total_consultation_all_causes', self.gf('django.db.models.fields.PositiveIntegerField')()),
            ('o5_total_suspected_malaria_cases', self.gf('django.db.models.fields.PositiveIntegerField')()),
            ('o5_total_tdr_tested_malaria_cases', self.gf('django.db.models.fields.PositiveIntegerField')()),
            ('o5_total_tdr_confirmed_malaria_cases', self.gf('django.db.models.fields.PositiveIntegerField')()),
            ('o5_total_tdr_parasite_pf_malaria_cases', self.gf('django.db.models.fields.PositiveIntegerField')()),
            ('o5_total_ge_tested_malaria_cases', self.gf('django.db.models.fields.PositiveIntegerField')()),
            ('o5_total_ge_confirmed_malaria_cases', self.gf('django.db.models.fields.PositiveIntegerField')()),
            ('o5_total_ge_parasite_pf_malaria_cases', self.gf('django.db.models.fields.PositiveIntegerField')()),
            ('o5_total_simple_malaria_cases', self.gf('django.db.models.fields.PositiveIntegerField')()),
            ('o5_total_severe_malaria_cases', self.gf('django.db.models.fields.PositiveIntegerField')()),
            ('o5_total_malaria_death', self.gf('django.db.models.fields.PositiveIntegerField')()),
            ('o5_total_death_all_causes', self.gf('django.db.models.fields.PositiveIntegerField')()),
            ('pw_total_consultation_all_causes', self.gf('django.db.models.fields.PositiveIntegerField')()),
            ('pw_total_suspected_malaria_cases', self.gf('django.db.models.fields.PositiveIntegerField')()),
            ('pw_total_tdr_tested_malaria_cases', self.gf('django.db.models.fields.PositiveIntegerField')()),
            ('pw_total_tdr_confirmed_malaria_cases', self.gf('django.db.models.fields.PositiveIntegerField')()),
            ('pw_total_tdr_parasite_pf_malaria_cases', self.gf('django.db.models.fields.PositiveIntegerField')()),
            ('pw_total_ge_tested_malaria_cases', self.gf('django.db.models.fields.PositiveIntegerField')()),
            ('pw_total_ge_confirmed_malaria_cases', self.gf('django.db.models.fields.PositiveIntegerField')()),
            ('pw_total_ge_parasite_pf_malaria_cases', self.gf('django.db.models.fields.PositiveIntegerField')()),
            ('pw_total_simple_malaria_cases', self.gf('django.db.models.fields.PositiveIntegerField')()),
            ('pw_total_severe_malaria_cases', self.gf('django.db.models.fields.PositiveIntegerField')()),
            ('pw_total_malaria_death', self.gf('django.db.models.fields.PositiveIntegerField')()),
            ('pw_total_death_all_causes', self.gf('django.db.models.fields.PositiveIntegerField')()),
        ))
        db.send_create_signal(u'snisi_malaria', ['AggEpidemioMalariaR'])

        # Adding M2M table for field agg_sources on 'AggEpidemioMalariaR'
        m2m_table_name = db.shorten_name(u'snisi_malaria_aggepidemiomalariar_agg_sources')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('from_aggepidemiomalariar', models.ForeignKey(orm[u'snisi_malaria.aggepidemiomalariar'], null=False)),
            ('to_aggepidemiomalariar', models.ForeignKey(orm[u'snisi_malaria.aggepidemiomalariar'], null=False))
        ))
        db.create_unique(m2m_table_name, ['from_aggepidemiomalariar_id', 'to_aggepidemiomalariar_id'])

        # Adding M2M table for field direct_agg_sources on 'AggEpidemioMalariaR'
        m2m_table_name = db.shorten_name(u'snisi_malaria_aggepidemiomalariar_direct_agg_sources')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('from_aggepidemiomalariar', models.ForeignKey(orm[u'snisi_malaria.aggepidemiomalariar'], null=False)),
            ('to_aggepidemiomalariar', models.ForeignKey(orm[u'snisi_malaria.aggepidemiomalariar'], null=False))
        ))
        db.create_unique(m2m_table_name, ['from_aggepidemiomalariar_id', 'to_aggepidemiomalariar_id'])

        # Adding M2M table for field indiv_sources on 'AggEpidemioMalariaR'
        m2m_table_name = db.shorten_name(u'snisi_malaria_aggepidemiomalariar_indiv_sources')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('aggepidemiomalariar', models.ForeignKey(orm[u'snisi_malaria.aggepidemiomalariar'], null=False)),
            ('epidemiomalariar', models.ForeignKey(orm[u'snisi_malaria.epidemiomalariar'], null=False))
        ))
        db.create_unique(m2m_table_name, ['aggepidemiomalariar_id', 'epidemiomalariar_id'])

        # Adding M2M table for field direct_indiv_sources on 'AggEpidemioMalariaR'
        m2m_table_name = db.shorten_name(u'snisi_malaria_aggepidemiomalariar_direct_indiv_sources')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('aggepidemiomalariar', models.ForeignKey(orm[u'snisi_malaria.aggepidemiomalariar'], null=False)),
            ('epidemiomalariar', models.ForeignKey(orm[u'snisi_malaria.epidemiomalariar'], null=False))
        ))
        db.create_unique(m2m_table_name, ['aggepidemiomalariar_id', 'epidemiomalariar_id'])


    def backwards(self, orm):
        # Deleting model 'MalariaR'
        db.delete_table(u'snisi_malaria_malariar')

        # Deleting model 'AggMalariaR'
        db.delete_table(u'snisi_malaria_aggmalariar')

        # Removing M2M table for field agg_sources on 'AggMalariaR'
        db.delete_table(db.shorten_name(u'snisi_malaria_aggmalariar_agg_sources'))

        # Removing M2M table for field direct_agg_sources on 'AggMalariaR'
        db.delete_table(db.shorten_name(u'snisi_malaria_aggmalariar_direct_agg_sources'))

        # Removing M2M table for field indiv_sources on 'AggMalariaR'
        db.delete_table(db.shorten_name(u'snisi_malaria_aggmalariar_indiv_sources'))

        # Removing M2M table for field direct_indiv_sources on 'AggMalariaR'
        db.delete_table(db.shorten_name(u'snisi_malaria_aggmalariar_direct_indiv_sources'))

        # Deleting model 'EpidemioMalariaR'
        db.delete_table(u'snisi_malaria_epidemiomalariar')

        # Deleting model 'AggEpidemioMalariaR'
        db.delete_table(u'snisi_malaria_aggepidemiomalariar')

        # Removing M2M table for field agg_sources on 'AggEpidemioMalariaR'
        db.delete_table(db.shorten_name(u'snisi_malaria_aggepidemiomalariar_agg_sources'))

        # Removing M2M table for field direct_agg_sources on 'AggEpidemioMalariaR'
        db.delete_table(db.shorten_name(u'snisi_malaria_aggepidemiomalariar_direct_agg_sources'))

        # Removing M2M table for field indiv_sources on 'AggEpidemioMalariaR'
        db.delete_table(db.shorten_name(u'snisi_malaria_aggepidemiomalariar_indiv_sources'))

        # Removing M2M table for field direct_indiv_sources on 'AggEpidemioMalariaR'
        db.delete_table(db.shorten_name(u'snisi_malaria_aggepidemiomalariar_direct_indiv_sources'))


    models = {
        u'auth.group': {
            'Meta': {'object_name': 'Group'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'})
        },
        u'auth.permission': {
            'Meta': {'ordering': "(u'content_type__app_label', u'content_type__model', u'codename')", 'unique_together': "((u'content_type', u'codename'),)", 'object_name': 'Permission'},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['contenttypes.ContentType']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        u'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        u'snisi_core.entity': {
            'Meta': {'object_name': 'Entity'},
            'active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'active_changed_on': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'geometry': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'latitude': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            u'level': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'}),
            u'lft': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'}),
            'longitude': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'parent': ('mptt.fields.TreeForeignKey', [], {'blank': 'True', 'related_name': "u'children'", 'null': 'True', 'to': u"orm['snisi_core.Entity']"}),
            u'rght': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '15', 'primary_key': 'True'}),
            u'tree_id': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'}),
            'type': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "u'entities'", 'to': u"orm['snisi_core.EntityType']"})
        },
        u'snisi_core.entitytype': {
            'Meta': {'object_name': 'EntityType'},
            'name': ('django.db.models.fields.CharField', [], {'max_length': '30'}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '15', 'primary_key': 'True'})
        },
        u'snisi_core.period': {
            'Meta': {'unique_together': "((u'start_on', u'end_on', u'period_type'),)", 'object_name': 'Period'},
            'end_on': ('django.db.models.fields.DateTimeField', [], {}),
            'identifier': ('django.db.models.fields.CharField', [], {'max_length': '200', 'primary_key': 'True'}),
            'period_type': ('django.db.models.fields.CharField', [], {'default': "u'custom'", 'max_length': '100'}),
            'start_on': ('django.db.models.fields.DateTimeField', [], {})
        },
        u'snisi_core.provider': {
            'Meta': {'object_name': 'Provider'},
            'access_since': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'null': 'True', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'gender': ('django.db.models.fields.CharField', [], {'default': "u'unknown'", 'max_length': '30'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "u'user_set'", 'blank': 'True', 'to': u"orm['auth.Group']"}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'location': ('django.db.models.fields.related.ForeignKey', [], {'default': "u'mali'", 'related_name': "u'contacts'", 'to': u"orm['snisi_core.Entity']"}),
            'maiden_name': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'middle_name': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'position': ('django.db.models.fields.CharField', [], {'max_length': '250', 'null': 'True', 'blank': 'True'}),
            'role': ('django.db.models.fields.related.ForeignKey', [], {'default': "u'guest'", 'to': u"orm['snisi_core.Role']"}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '50', 'null': 'True', 'blank': 'True'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "u'user_set'", 'blank': 'True', 'to': u"orm['auth.Permission']"}),
            'username': ('django.db.models.fields.CharField', [], {'max_length': '50', 'primary_key': 'True'})
        },
        u'snisi_core.role': {
            'Meta': {'object_name': 'Role'},
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '15', 'primary_key': 'True'})
        },
        u'snisi_core.snisireport': {
            'Meta': {'object_name': 'SNISIReport'},
            'arrival_status': ('django.db.models.fields.CharField', [], {'default': "u'not_applicable'", 'max_length': '40'}),
            'auto_validated': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'completed_on': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'completion_status': ('django.db.models.fields.CharField', [], {'default': "u'incomplete'", 'max_length': '40'}),
            'created_by': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "u'snisi_core_snisireport_reports'", 'to': u"orm['snisi_core.Provider']"}),
            'created_on': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'entity': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "u'snisi_core_snisireport_reports'", 'null': 'True', 'to': u"orm['snisi_core.Entity']"}),
            'integrity_status': ('django.db.models.fields.CharField', [], {'default': "u'not_checked'", 'max_length': '40'}),
            'modified_by': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "u'own_modified_reports'", 'null': 'True', 'to': u"orm['snisi_core.Provider']"}),
            'modified_on': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'period': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "u'snisi_core_snisireport_reports'", 'null': 'True', 'to': u"orm['snisi_core.Period']"}),
            'receipt': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '200'}),
            'report_cls': ('django.db.models.fields.CharField', [], {'max_length': '512', 'null': 'True', 'blank': 'True'}),
            'uuid': ('django.db.models.fields.CharField', [], {'default': "'00566109-4e96-4a7d-809f-960e79fe82df'", 'max_length': '200', 'primary_key': 'True'}),
            'validated_by': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "u'own_validated_reports'", 'null': 'True', 'to': u"orm['snisi_core.Provider']"}),
            'validated_on': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'validation_status': ('django.db.models.fields.CharField', [], {'default': "u'not_applicable'", 'max_length': '40'})
        },
        u'snisi_malaria.aggepidemiomalariar': {
            'Meta': {'object_name': 'AggEpidemioMalariaR', '_ormbases': [u'snisi_core.SNISIReport']},
            'agg_sources': ('django.db.models.fields.related.ManyToManyField', [], {'blank': 'True', 'related_name': "'agg_sources_rel_+'", 'null': 'True', 'to': u"orm['snisi_malaria.AggEpidemioMalariaR']"}),
            'direct_agg_sources': ('django.db.models.fields.related.ManyToManyField', [], {'blank': 'True', 'related_name': "'direct_agg_sources_rel_+'", 'null': 'True', 'to': u"orm['snisi_malaria.AggEpidemioMalariaR']"}),
            'direct_indiv_sources': ('django.db.models.fields.related.ManyToManyField', [], {'blank': 'True', 'related_name': "u'direct_source_agg_aggepidemiomalariar_reports'", 'null': 'True', 'symmetrical': 'False', 'to': u"orm['snisi_malaria.EpidemioMalariaR']"}),
            'indiv_sources': ('django.db.models.fields.related.ManyToManyField', [], {'blank': 'True', 'related_name': "u'source_agg_aggepidemiomalariar_reports'", 'null': 'True', 'symmetrical': 'False', 'to': u"orm['snisi_malaria.EpidemioMalariaR']"}),
            'nb_agg_reports_altered': ('django.db.models.fields.PositiveIntegerField', [], {'null': 'True', 'blank': 'True'}),
            'nb_agg_reports_auto_validated': ('django.db.models.fields.PositiveIntegerField', [], {'null': 'True', 'blank': 'True'}),
            'nb_agg_reports_validated': ('django.db.models.fields.PositiveIntegerField', [], {'null': 'True', 'blank': 'True'}),
            'nb_source_reports_altered': ('django.db.models.fields.PositiveIntegerField', [], {'null': 'True', 'blank': 'True'}),
            'nb_source_reports_arrived': ('django.db.models.fields.PositiveIntegerField', [], {'null': 'True', 'blank': 'True'}),
            'nb_source_reports_arrived_complete': ('django.db.models.fields.PositiveIntegerField', [], {'null': 'True', 'blank': 'True'}),
            'nb_source_reports_arrived_correct': ('django.db.models.fields.PositiveIntegerField', [], {'null': 'True', 'blank': 'True'}),
            'nb_source_reports_arrived_on_time': ('django.db.models.fields.PositiveIntegerField', [], {'null': 'True', 'blank': 'True'}),
            'nb_source_reports_auto_validated': ('django.db.models.fields.PositiveIntegerField', [], {'null': 'True', 'blank': 'True'}),
            'nb_source_reports_expected': ('django.db.models.fields.PositiveIntegerField', [], {'null': 'True', 'blank': 'True'}),
            'nb_source_reports_validated': ('django.db.models.fields.PositiveIntegerField', [], {'null': 'True', 'blank': 'True'}),
            'o5_total_consultation_all_causes': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'o5_total_death_all_causes': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'o5_total_ge_confirmed_malaria_cases': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'o5_total_ge_parasite_pf_malaria_cases': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'o5_total_ge_tested_malaria_cases': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'o5_total_malaria_death': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'o5_total_severe_malaria_cases': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'o5_total_simple_malaria_cases': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'o5_total_suspected_malaria_cases': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'o5_total_tdr_confirmed_malaria_cases': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'o5_total_tdr_parasite_pf_malaria_cases': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'o5_total_tdr_tested_malaria_cases': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'pw_total_consultation_all_causes': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'pw_total_death_all_causes': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'pw_total_ge_confirmed_malaria_cases': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'pw_total_ge_parasite_pf_malaria_cases': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'pw_total_ge_tested_malaria_cases': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'pw_total_malaria_death': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'pw_total_severe_malaria_cases': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'pw_total_simple_malaria_cases': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'pw_total_suspected_malaria_cases': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'pw_total_tdr_confirmed_malaria_cases': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'pw_total_tdr_parasite_pf_malaria_cases': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'pw_total_tdr_tested_malaria_cases': ('django.db.models.fields.PositiveIntegerField', [], {}),
            u'snisireport_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['snisi_core.SNISIReport']", 'unique': 'True', 'primary_key': 'True'}),
            'u5_total_consultation_all_causes': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'u5_total_death_all_causes': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'u5_total_ge_confirmed_malaria_cases': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'u5_total_ge_parasite_pf_malaria_cases': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'u5_total_ge_tested_malaria_cases': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'u5_total_malaria_death': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'u5_total_severe_malaria_cases': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'u5_total_simple_malaria_cases': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'u5_total_suspected_malaria_cases': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'u5_total_tdr_confirmed_malaria_cases': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'u5_total_tdr_parasite_pf_malaria_cases': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'u5_total_tdr_tested_malaria_cases': ('django.db.models.fields.PositiveIntegerField', [], {})
        },
        u'snisi_malaria.aggmalariar': {
            'Meta': {'object_name': 'AggMalariaR', '_ormbases': [u'snisi_core.SNISIReport']},
            'agg_sources': ('django.db.models.fields.related.ManyToManyField', [], {'blank': 'True', 'related_name': "'agg_sources_rel_+'", 'null': 'True', 'to': u"orm['snisi_malaria.AggMalariaR']"}),
            'direct_agg_sources': ('django.db.models.fields.related.ManyToManyField', [], {'blank': 'True', 'related_name': "'direct_agg_sources_rel_+'", 'null': 'True', 'to': u"orm['snisi_malaria.AggMalariaR']"}),
            'direct_indiv_sources': ('django.db.models.fields.related.ManyToManyField', [], {'blank': 'True', 'related_name': "u'direct_source_agg_aggmalariar_reports'", 'null': 'True', 'symmetrical': 'False', 'to': u"orm['snisi_malaria.MalariaR']"}),
            'indiv_sources': ('django.db.models.fields.related.ManyToManyField', [], {'blank': 'True', 'related_name': "u'source_agg_aggmalariar_reports'", 'null': 'True', 'symmetrical': 'False', 'to': u"orm['snisi_malaria.MalariaR']"}),
            'nb_agg_reports_altered': ('django.db.models.fields.PositiveIntegerField', [], {'null': 'True', 'blank': 'True'}),
            'nb_agg_reports_auto_validated': ('django.db.models.fields.PositiveIntegerField', [], {'null': 'True', 'blank': 'True'}),
            'nb_agg_reports_validated': ('django.db.models.fields.PositiveIntegerField', [], {'null': 'True', 'blank': 'True'}),
            'nb_source_reports_altered': ('django.db.models.fields.PositiveIntegerField', [], {'null': 'True', 'blank': 'True'}),
            'nb_source_reports_arrived': ('django.db.models.fields.PositiveIntegerField', [], {'null': 'True', 'blank': 'True'}),
            'nb_source_reports_arrived_complete': ('django.db.models.fields.PositiveIntegerField', [], {'null': 'True', 'blank': 'True'}),
            'nb_source_reports_arrived_correct': ('django.db.models.fields.PositiveIntegerField', [], {'null': 'True', 'blank': 'True'}),
            'nb_source_reports_arrived_on_time': ('django.db.models.fields.PositiveIntegerField', [], {'null': 'True', 'blank': 'True'}),
            'nb_source_reports_auto_validated': ('django.db.models.fields.PositiveIntegerField', [], {'null': 'True', 'blank': 'True'}),
            'nb_source_reports_expected': ('django.db.models.fields.PositiveIntegerField', [], {'null': 'True', 'blank': 'True'}),
            'nb_source_reports_validated': ('django.db.models.fields.PositiveIntegerField', [], {'null': 'True', 'blank': 'True'}),
            'o5_total_confirmed_malaria_cases': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'o5_total_consultation_all_causes': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'o5_total_death_all_causes': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'o5_total_inpatient_all_causes': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'o5_total_malaria_death': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'o5_total_malaria_inpatient': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'o5_total_severe_malaria_cases': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'o5_total_simple_malaria_cases': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'o5_total_suspected_malaria_cases': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'o5_total_tested_malaria_cases': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'o5_total_treated_malaria_cases': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'pw_total_anc1': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'pw_total_confirmed_malaria_cases': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'pw_total_consultation_all_causes': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'pw_total_death_all_causes': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'pw_total_distributed_bednets': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'pw_total_inpatient_all_causes': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'pw_total_malaria_death': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'pw_total_malaria_inpatient': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'pw_total_severe_malaria_cases': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'pw_total_sp1': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'pw_total_sp2': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'pw_total_suspected_malaria_cases': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'pw_total_tested_malaria_cases': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'pw_total_treated_malaria_cases': ('django.db.models.fields.PositiveIntegerField', [], {}),
            u'snisireport_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['snisi_core.SNISIReport']", 'unique': 'True', 'primary_key': 'True'}),
            'stockout_act_adult': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'stockout_act_children': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'stockout_act_youth': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'stockout_artemether': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'stockout_bednet': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'stockout_quinine': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'stockout_rdt': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'stockout_serum': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'stockout_sp': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'u5_total_confirmed_malaria_cases': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'u5_total_consultation_all_causes': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'u5_total_death_all_causes': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'u5_total_distributed_bednets': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'u5_total_inpatient_all_causes': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'u5_total_malaria_death': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'u5_total_malaria_inpatient': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'u5_total_severe_malaria_cases': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'u5_total_simple_malaria_cases': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'u5_total_suspected_malaria_cases': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'u5_total_tested_malaria_cases': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'u5_total_treated_malaria_cases': ('django.db.models.fields.PositiveIntegerField', [], {})
        },
        u'snisi_malaria.epidemiomalariar': {
            'Meta': {'object_name': 'EpidemioMalariaR', '_ormbases': [u'snisi_core.SNISIReport']},
            'o5_total_consultation_all_causes': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'o5_total_death_all_causes': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'o5_total_ge_confirmed_malaria_cases': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'o5_total_ge_parasite_pf_malaria_cases': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'o5_total_ge_tested_malaria_cases': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'o5_total_malaria_death': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'o5_total_severe_malaria_cases': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'o5_total_simple_malaria_cases': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'o5_total_suspected_malaria_cases': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'o5_total_tdr_confirmed_malaria_cases': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'o5_total_tdr_parasite_pf_malaria_cases': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'o5_total_tdr_tested_malaria_cases': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'pw_total_consultation_all_causes': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'pw_total_death_all_causes': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'pw_total_ge_confirmed_malaria_cases': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'pw_total_ge_parasite_pf_malaria_cases': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'pw_total_ge_tested_malaria_cases': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'pw_total_malaria_death': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'pw_total_severe_malaria_cases': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'pw_total_simple_malaria_cases': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'pw_total_suspected_malaria_cases': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'pw_total_tdr_confirmed_malaria_cases': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'pw_total_tdr_parasite_pf_malaria_cases': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'pw_total_tdr_tested_malaria_cases': ('django.db.models.fields.PositiveIntegerField', [], {}),
            u'snisireport_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['snisi_core.SNISIReport']", 'unique': 'True', 'primary_key': 'True'}),
            'u5_total_consultation_all_causes': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'u5_total_death_all_causes': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'u5_total_ge_confirmed_malaria_cases': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'u5_total_ge_parasite_pf_malaria_cases': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'u5_total_ge_tested_malaria_cases': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'u5_total_malaria_death': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'u5_total_severe_malaria_cases': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'u5_total_simple_malaria_cases': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'u5_total_suspected_malaria_cases': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'u5_total_tdr_confirmed_malaria_cases': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'u5_total_tdr_parasite_pf_malaria_cases': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'u5_total_tdr_tested_malaria_cases': ('django.db.models.fields.PositiveIntegerField', [], {})
        },
        u'snisi_malaria.malariar': {
            'Meta': {'object_name': 'MalariaR', '_ormbases': [u'snisi_core.SNISIReport']},
            'o5_total_confirmed_malaria_cases': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'o5_total_consultation_all_causes': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'o5_total_death_all_causes': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'o5_total_inpatient_all_causes': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'o5_total_malaria_death': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'o5_total_malaria_inpatient': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'o5_total_severe_malaria_cases': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'o5_total_simple_malaria_cases': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'o5_total_suspected_malaria_cases': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'o5_total_tested_malaria_cases': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'o5_total_treated_malaria_cases': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'pw_total_anc1': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'pw_total_confirmed_malaria_cases': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'pw_total_consultation_all_causes': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'pw_total_death_all_causes': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'pw_total_distributed_bednets': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'pw_total_inpatient_all_causes': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'pw_total_malaria_death': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'pw_total_malaria_inpatient': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'pw_total_severe_malaria_cases': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'pw_total_sp1': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'pw_total_sp2': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'pw_total_suspected_malaria_cases': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'pw_total_tested_malaria_cases': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'pw_total_treated_malaria_cases': ('django.db.models.fields.PositiveIntegerField', [], {}),
            u'snisireport_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['snisi_core.SNISIReport']", 'unique': 'True', 'primary_key': 'True'}),
            'stockout_act_adult': ('django.db.models.fields.CharField', [], {'max_length': '1'}),
            'stockout_act_children': ('django.db.models.fields.CharField', [], {'max_length': '1'}),
            'stockout_act_youth': ('django.db.models.fields.CharField', [], {'max_length': '1'}),
            'stockout_artemether': ('django.db.models.fields.CharField', [], {'max_length': '1'}),
            'stockout_bednet': ('django.db.models.fields.CharField', [], {'max_length': '1'}),
            'stockout_quinine': ('django.db.models.fields.CharField', [], {'max_length': '1'}),
            'stockout_rdt': ('django.db.models.fields.CharField', [], {'max_length': '1'}),
            'stockout_serum': ('django.db.models.fields.CharField', [], {'max_length': '1'}),
            'stockout_sp': ('django.db.models.fields.CharField', [], {'max_length': '1'}),
            'u5_total_confirmed_malaria_cases': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'u5_total_consultation_all_causes': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'u5_total_death_all_causes': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'u5_total_distributed_bednets': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'u5_total_inpatient_all_causes': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'u5_total_malaria_death': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'u5_total_malaria_inpatient': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'u5_total_severe_malaria_cases': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'u5_total_simple_malaria_cases': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'u5_total_suspected_malaria_cases': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'u5_total_tested_malaria_cases': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'u5_total_treated_malaria_cases': ('django.db.models.fields.PositiveIntegerField', [], {})
        }
    }

    complete_apps = ['snisi_malaria']