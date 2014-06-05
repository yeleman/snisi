# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'ProvidedServicesR'
        db.create_table(u'snisi_reprohealth_providedservicesr', (
            (u'snisireport_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['snisi_core.SNISIReport'], unique=True, primary_key=True)),
            ('tubal_ligations', self.gf('django.db.models.fields.PositiveIntegerField')()),
            ('intrauterine_devices', self.gf('django.db.models.fields.PositiveIntegerField')()),
            ('injections', self.gf('django.db.models.fields.PositiveIntegerField')()),
            ('pills', self.gf('django.db.models.fields.PositiveIntegerField')()),
            ('male_condoms', self.gf('django.db.models.fields.PositiveIntegerField')()),
            ('female_condoms', self.gf('django.db.models.fields.PositiveIntegerField')()),
            ('emergency_controls', self.gf('django.db.models.fields.PositiveIntegerField')()),
            ('implants', self.gf('django.db.models.fields.PositiveIntegerField')()),
            ('new_clients', self.gf('django.db.models.fields.PositiveIntegerField')()),
            ('previous_clients', self.gf('django.db.models.fields.PositiveIntegerField')()),
            ('under25_visits', self.gf('django.db.models.fields.PositiveIntegerField')()),
            ('over25_visits', self.gf('django.db.models.fields.PositiveIntegerField')()),
            ('very_first_visits', self.gf('django.db.models.fields.PositiveIntegerField')()),
            ('short_term_method_visits', self.gf('django.db.models.fields.PositiveIntegerField')()),
            ('long_term_method_visits', self.gf('django.db.models.fields.PositiveIntegerField')()),
            ('hiv_counseling_clients', self.gf('django.db.models.fields.PositiveIntegerField')()),
            ('hiv_tests', self.gf('django.db.models.fields.PositiveIntegerField')()),
            ('hiv_positive_results', self.gf('django.db.models.fields.PositiveIntegerField')()),
            ('implant_removals', self.gf('django.db.models.fields.PositiveIntegerField')()),
            ('iud_removal', self.gf('django.db.models.fields.PositiveIntegerField')()),
        ))
        db.send_create_signal(u'snisi_reprohealth', ['ProvidedServicesR'])

        # Adding model 'AggProvidedServicesR'
        db.create_table(u'snisi_reprohealth_aggprovidedservicesr', (
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
            ('tubal_ligations', self.gf('django.db.models.fields.PositiveIntegerField')()),
            ('intrauterine_devices', self.gf('django.db.models.fields.PositiveIntegerField')()),
            ('injections', self.gf('django.db.models.fields.PositiveIntegerField')()),
            ('pills', self.gf('django.db.models.fields.PositiveIntegerField')()),
            ('male_condoms', self.gf('django.db.models.fields.PositiveIntegerField')()),
            ('female_condoms', self.gf('django.db.models.fields.PositiveIntegerField')()),
            ('emergency_controls', self.gf('django.db.models.fields.PositiveIntegerField')()),
            ('implants', self.gf('django.db.models.fields.PositiveIntegerField')()),
            ('new_clients', self.gf('django.db.models.fields.PositiveIntegerField')()),
            ('previous_clients', self.gf('django.db.models.fields.PositiveIntegerField')()),
            ('under25_visits', self.gf('django.db.models.fields.PositiveIntegerField')()),
            ('over25_visits', self.gf('django.db.models.fields.PositiveIntegerField')()),
            ('very_first_visits', self.gf('django.db.models.fields.PositiveIntegerField')()),
            ('short_term_method_visits', self.gf('django.db.models.fields.PositiveIntegerField')()),
            ('long_term_method_visits', self.gf('django.db.models.fields.PositiveIntegerField')()),
            ('hiv_counseling_clients', self.gf('django.db.models.fields.PositiveIntegerField')()),
            ('hiv_tests', self.gf('django.db.models.fields.PositiveIntegerField')()),
            ('hiv_positive_results', self.gf('django.db.models.fields.PositiveIntegerField')()),
            ('implant_removals', self.gf('django.db.models.fields.PositiveIntegerField')()),
            ('iud_removal', self.gf('django.db.models.fields.PositiveIntegerField')()),
        ))
        db.send_create_signal(u'snisi_reprohealth', ['AggProvidedServicesR'])

        # Adding M2M table for field agg_sources on 'AggProvidedServicesR'
        m2m_table_name = db.shorten_name(u'snisi_reprohealth_aggprovidedservicesr_agg_sources')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('from_aggprovidedservicesr', models.ForeignKey(orm[u'snisi_reprohealth.aggprovidedservicesr'], null=False)),
            ('to_aggprovidedservicesr', models.ForeignKey(orm[u'snisi_reprohealth.aggprovidedservicesr'], null=False))
        ))
        db.create_unique(m2m_table_name, ['from_aggprovidedservicesr_id', 'to_aggprovidedservicesr_id'])

        # Adding M2M table for field direct_agg_sources on 'AggProvidedServicesR'
        m2m_table_name = db.shorten_name(u'snisi_reprohealth_aggprovidedservicesr_direct_agg_sources')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('from_aggprovidedservicesr', models.ForeignKey(orm[u'snisi_reprohealth.aggprovidedservicesr'], null=False)),
            ('to_aggprovidedservicesr', models.ForeignKey(orm[u'snisi_reprohealth.aggprovidedservicesr'], null=False))
        ))
        db.create_unique(m2m_table_name, ['from_aggprovidedservicesr_id', 'to_aggprovidedservicesr_id'])

        # Adding M2M table for field indiv_sources on 'AggProvidedServicesR'
        m2m_table_name = db.shorten_name(u'snisi_reprohealth_aggprovidedservicesr_indiv_sources')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('aggprovidedservicesr', models.ForeignKey(orm[u'snisi_reprohealth.aggprovidedservicesr'], null=False)),
            ('providedservicesr', models.ForeignKey(orm[u'snisi_reprohealth.providedservicesr'], null=False))
        ))
        db.create_unique(m2m_table_name, ['aggprovidedservicesr_id', 'providedservicesr_id'])

        # Adding M2M table for field direct_indiv_sources on 'AggProvidedServicesR'
        m2m_table_name = db.shorten_name(u'snisi_reprohealth_aggprovidedservicesr_direct_indiv_sources')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('aggprovidedservicesr', models.ForeignKey(orm[u'snisi_reprohealth.aggprovidedservicesr'], null=False)),
            ('providedservicesr', models.ForeignKey(orm[u'snisi_reprohealth.providedservicesr'], null=False))
        ))
        db.create_unique(m2m_table_name, ['aggprovidedservicesr_id', 'providedservicesr_id'])

        # Adding model 'FinancialR'
        db.create_table(u'snisi_reprohealth_financialr', (
            (u'snisireport_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['snisi_core.SNISIReport'], unique=True, primary_key=True)),
            ('intrauterine_devices_qty', self.gf('django.db.models.fields.PositiveIntegerField')()),
            ('intrauterine_devices_price', self.gf('django.db.models.fields.PositiveIntegerField')()),
            ('intrauterine_devices_revenue', self.gf('django.db.models.fields.PositiveIntegerField')()),
            ('implants_qty', self.gf('django.db.models.fields.PositiveIntegerField')()),
            ('implants_price', self.gf('django.db.models.fields.PositiveIntegerField')()),
            ('implants_revenue', self.gf('django.db.models.fields.PositiveIntegerField')()),
            ('injections_qty', self.gf('django.db.models.fields.PositiveIntegerField')()),
            ('injections_price', self.gf('django.db.models.fields.PositiveIntegerField')()),
            ('injections_revenue', self.gf('django.db.models.fields.PositiveIntegerField')()),
            ('pills_qty', self.gf('django.db.models.fields.PositiveIntegerField')()),
            ('pills_price', self.gf('django.db.models.fields.PositiveIntegerField')()),
            ('pills_revenue', self.gf('django.db.models.fields.PositiveIntegerField')()),
            ('male_condoms_qty', self.gf('django.db.models.fields.PositiveIntegerField')()),
            ('male_condoms_price', self.gf('django.db.models.fields.PositiveIntegerField')()),
            ('male_condoms_revenue', self.gf('django.db.models.fields.PositiveIntegerField')()),
            ('female_condoms_qty', self.gf('django.db.models.fields.PositiveIntegerField')()),
            ('female_condoms_price', self.gf('django.db.models.fields.PositiveIntegerField')()),
            ('female_condoms_revenue', self.gf('django.db.models.fields.PositiveIntegerField')()),
            ('hiv_tests_qty', self.gf('django.db.models.fields.PositiveIntegerField')()),
            ('hiv_tests_price', self.gf('django.db.models.fields.PositiveIntegerField')()),
            ('hiv_tests_revenue', self.gf('django.db.models.fields.PositiveIntegerField')()),
            ('iud_removal_qty', self.gf('django.db.models.fields.PositiveIntegerField')()),
            ('iud_removal_price', self.gf('django.db.models.fields.PositiveIntegerField')()),
            ('iud_removal_revenue', self.gf('django.db.models.fields.PositiveIntegerField')()),
            ('implant_removal_qty', self.gf('django.db.models.fields.PositiveIntegerField')()),
            ('implant_removal_price', self.gf('django.db.models.fields.PositiveIntegerField')()),
            ('implant_removal_revenue', self.gf('django.db.models.fields.PositiveIntegerField')()),
        ))
        db.send_create_signal(u'snisi_reprohealth', ['FinancialR'])

        # Adding model 'AggFinancialR'
        db.create_table(u'snisi_reprohealth_aggfinancialr', (
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
            ('intrauterine_devices_qty', self.gf('django.db.models.fields.PositiveIntegerField')()),
            ('intrauterine_devices_price', self.gf('django.db.models.fields.PositiveIntegerField')()),
            ('intrauterine_devices_revenue', self.gf('django.db.models.fields.PositiveIntegerField')()),
            ('implants_qty', self.gf('django.db.models.fields.PositiveIntegerField')()),
            ('implants_price', self.gf('django.db.models.fields.PositiveIntegerField')()),
            ('implants_revenue', self.gf('django.db.models.fields.PositiveIntegerField')()),
            ('injections_qty', self.gf('django.db.models.fields.PositiveIntegerField')()),
            ('injections_price', self.gf('django.db.models.fields.PositiveIntegerField')()),
            ('injections_revenue', self.gf('django.db.models.fields.PositiveIntegerField')()),
            ('pills_qty', self.gf('django.db.models.fields.PositiveIntegerField')()),
            ('pills_price', self.gf('django.db.models.fields.PositiveIntegerField')()),
            ('pills_revenue', self.gf('django.db.models.fields.PositiveIntegerField')()),
            ('male_condoms_qty', self.gf('django.db.models.fields.PositiveIntegerField')()),
            ('male_condoms_price', self.gf('django.db.models.fields.PositiveIntegerField')()),
            ('male_condoms_revenue', self.gf('django.db.models.fields.PositiveIntegerField')()),
            ('female_condoms_qty', self.gf('django.db.models.fields.PositiveIntegerField')()),
            ('female_condoms_price', self.gf('django.db.models.fields.PositiveIntegerField')()),
            ('female_condoms_revenue', self.gf('django.db.models.fields.PositiveIntegerField')()),
            ('hiv_tests_qty', self.gf('django.db.models.fields.PositiveIntegerField')()),
            ('hiv_tests_price', self.gf('django.db.models.fields.PositiveIntegerField')()),
            ('hiv_tests_revenue', self.gf('django.db.models.fields.PositiveIntegerField')()),
            ('iud_removal_qty', self.gf('django.db.models.fields.PositiveIntegerField')()),
            ('iud_removal_price', self.gf('django.db.models.fields.PositiveIntegerField')()),
            ('iud_removal_revenue', self.gf('django.db.models.fields.PositiveIntegerField')()),
            ('implant_removal_qty', self.gf('django.db.models.fields.PositiveIntegerField')()),
            ('implant_removal_price', self.gf('django.db.models.fields.PositiveIntegerField')()),
            ('implant_removal_revenue', self.gf('django.db.models.fields.PositiveIntegerField')()),
        ))
        db.send_create_signal(u'snisi_reprohealth', ['AggFinancialR'])

        # Adding M2M table for field agg_sources on 'AggFinancialR'
        m2m_table_name = db.shorten_name(u'snisi_reprohealth_aggfinancialr_agg_sources')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('from_aggfinancialr', models.ForeignKey(orm[u'snisi_reprohealth.aggfinancialr'], null=False)),
            ('to_aggfinancialr', models.ForeignKey(orm[u'snisi_reprohealth.aggfinancialr'], null=False))
        ))
        db.create_unique(m2m_table_name, ['from_aggfinancialr_id', 'to_aggfinancialr_id'])

        # Adding M2M table for field direct_agg_sources on 'AggFinancialR'
        m2m_table_name = db.shorten_name(u'snisi_reprohealth_aggfinancialr_direct_agg_sources')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('from_aggfinancialr', models.ForeignKey(orm[u'snisi_reprohealth.aggfinancialr'], null=False)),
            ('to_aggfinancialr', models.ForeignKey(orm[u'snisi_reprohealth.aggfinancialr'], null=False))
        ))
        db.create_unique(m2m_table_name, ['from_aggfinancialr_id', 'to_aggfinancialr_id'])

        # Adding M2M table for field indiv_sources on 'AggFinancialR'
        m2m_table_name = db.shorten_name(u'snisi_reprohealth_aggfinancialr_indiv_sources')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('aggfinancialr', models.ForeignKey(orm[u'snisi_reprohealth.aggfinancialr'], null=False)),
            ('financialr', models.ForeignKey(orm[u'snisi_reprohealth.financialr'], null=False))
        ))
        db.create_unique(m2m_table_name, ['aggfinancialr_id', 'financialr_id'])

        # Adding M2M table for field direct_indiv_sources on 'AggFinancialR'
        m2m_table_name = db.shorten_name(u'snisi_reprohealth_aggfinancialr_direct_indiv_sources')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('aggfinancialr', models.ForeignKey(orm[u'snisi_reprohealth.aggfinancialr'], null=False)),
            ('financialr', models.ForeignKey(orm[u'snisi_reprohealth.financialr'], null=False))
        ))
        db.create_unique(m2m_table_name, ['aggfinancialr_id', 'financialr_id'])

        # Adding model 'ContraceptiveStockR'
        db.create_table(u'snisi_reprohealth_contraceptivestockr', (
            (u'snisireport_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['snisi_core.SNISIReport'], unique=True, primary_key=True)),
            ('intrauterine_devices_initial', self.gf('django.db.models.fields.PositiveIntegerField')()),
            ('intrauterine_devices_used', self.gf('django.db.models.fields.PositiveIntegerField')()),
            ('intrauterine_devices_received', self.gf('django.db.models.fields.PositiveIntegerField')()),
            ('implants_initial', self.gf('django.db.models.fields.PositiveIntegerField')()),
            ('implants_used', self.gf('django.db.models.fields.PositiveIntegerField')()),
            ('implants_received', self.gf('django.db.models.fields.PositiveIntegerField')()),
            ('injections_initial', self.gf('django.db.models.fields.PositiveIntegerField')()),
            ('injections_used', self.gf('django.db.models.fields.PositiveIntegerField')()),
            ('injections_received', self.gf('django.db.models.fields.PositiveIntegerField')()),
            ('pills_initial', self.gf('django.db.models.fields.PositiveIntegerField')()),
            ('pills_used', self.gf('django.db.models.fields.PositiveIntegerField')()),
            ('pills_received', self.gf('django.db.models.fields.PositiveIntegerField')()),
            ('male_condoms_initial', self.gf('django.db.models.fields.PositiveIntegerField')()),
            ('male_condoms_used', self.gf('django.db.models.fields.PositiveIntegerField')()),
            ('male_condoms_received', self.gf('django.db.models.fields.PositiveIntegerField')()),
            ('female_condoms_initial', self.gf('django.db.models.fields.PositiveIntegerField')()),
            ('female_condoms_used', self.gf('django.db.models.fields.PositiveIntegerField')()),
            ('female_condoms_received', self.gf('django.db.models.fields.PositiveIntegerField')()),
            ('hiv_tests_initial', self.gf('django.db.models.fields.PositiveIntegerField')()),
            ('hiv_tests_used', self.gf('django.db.models.fields.PositiveIntegerField')()),
            ('hiv_tests_received', self.gf('django.db.models.fields.PositiveIntegerField')()),
            ('intrauterine_devices_observation', self.gf('django.db.models.fields.CharField')(max_length=500, null=True, blank=True)),
            ('implants_observation', self.gf('django.db.models.fields.CharField')(max_length=500, null=True, blank=True)),
            ('injections_observation', self.gf('django.db.models.fields.CharField')(max_length=500, null=True, blank=True)),
            ('pills_observation', self.gf('django.db.models.fields.CharField')(max_length=500, null=True, blank=True)),
            ('male_condoms_observation', self.gf('django.db.models.fields.CharField')(max_length=500, null=True, blank=True)),
            ('female_condoms_observation', self.gf('django.db.models.fields.CharField')(max_length=500, null=True, blank=True)),
            ('hiv_tests_observation', self.gf('django.db.models.fields.CharField')(max_length=500, null=True, blank=True)),
        ))
        db.send_create_signal(u'snisi_reprohealth', ['ContraceptiveStockR'])

        # Adding model 'AggContraceptiveStockR'
        db.create_table(u'snisi_reprohealth_aggcontraceptivestockr', (
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
            ('intrauterine_devices_initial', self.gf('django.db.models.fields.PositiveIntegerField')()),
            ('intrauterine_devices_used', self.gf('django.db.models.fields.PositiveIntegerField')()),
            ('intrauterine_devices_received', self.gf('django.db.models.fields.PositiveIntegerField')()),
            ('implants_initial', self.gf('django.db.models.fields.PositiveIntegerField')()),
            ('implants_used', self.gf('django.db.models.fields.PositiveIntegerField')()),
            ('implants_received', self.gf('django.db.models.fields.PositiveIntegerField')()),
            ('injections_initial', self.gf('django.db.models.fields.PositiveIntegerField')()),
            ('injections_used', self.gf('django.db.models.fields.PositiveIntegerField')()),
            ('injections_received', self.gf('django.db.models.fields.PositiveIntegerField')()),
            ('pills_initial', self.gf('django.db.models.fields.PositiveIntegerField')()),
            ('pills_used', self.gf('django.db.models.fields.PositiveIntegerField')()),
            ('pills_received', self.gf('django.db.models.fields.PositiveIntegerField')()),
            ('male_condoms_initial', self.gf('django.db.models.fields.PositiveIntegerField')()),
            ('male_condoms_used', self.gf('django.db.models.fields.PositiveIntegerField')()),
            ('male_condoms_received', self.gf('django.db.models.fields.PositiveIntegerField')()),
            ('female_condoms_initial', self.gf('django.db.models.fields.PositiveIntegerField')()),
            ('female_condoms_used', self.gf('django.db.models.fields.PositiveIntegerField')()),
            ('female_condoms_received', self.gf('django.db.models.fields.PositiveIntegerField')()),
            ('hiv_tests_initial', self.gf('django.db.models.fields.PositiveIntegerField')()),
            ('hiv_tests_used', self.gf('django.db.models.fields.PositiveIntegerField')()),
            ('hiv_tests_received', self.gf('django.db.models.fields.PositiveIntegerField')()),
        ))
        db.send_create_signal(u'snisi_reprohealth', ['AggContraceptiveStockR'])

        # Adding M2M table for field agg_sources on 'AggContraceptiveStockR'
        m2m_table_name = db.shorten_name(u'snisi_reprohealth_aggcontraceptivestockr_agg_sources')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('from_aggcontraceptivestockr', models.ForeignKey(orm[u'snisi_reprohealth.aggcontraceptivestockr'], null=False)),
            ('to_aggcontraceptivestockr', models.ForeignKey(orm[u'snisi_reprohealth.aggcontraceptivestockr'], null=False))
        ))
        db.create_unique(m2m_table_name, ['from_aggcontraceptivestockr_id', 'to_aggcontraceptivestockr_id'])

        # Adding M2M table for field direct_agg_sources on 'AggContraceptiveStockR'
        m2m_table_name = db.shorten_name(u'snisi_reprohealth_aggcontraceptivestockr_direct_agg_sources')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('from_aggcontraceptivestockr', models.ForeignKey(orm[u'snisi_reprohealth.aggcontraceptivestockr'], null=False)),
            ('to_aggcontraceptivestockr', models.ForeignKey(orm[u'snisi_reprohealth.aggcontraceptivestockr'], null=False))
        ))
        db.create_unique(m2m_table_name, ['from_aggcontraceptivestockr_id', 'to_aggcontraceptivestockr_id'])

        # Adding M2M table for field indiv_sources on 'AggContraceptiveStockR'
        m2m_table_name = db.shorten_name(u'snisi_reprohealth_aggcontraceptivestockr_indiv_sources')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('aggcontraceptivestockr', models.ForeignKey(orm[u'snisi_reprohealth.aggcontraceptivestockr'], null=False)),
            ('contraceptivestockr', models.ForeignKey(orm[u'snisi_reprohealth.contraceptivestockr'], null=False))
        ))
        db.create_unique(m2m_table_name, ['aggcontraceptivestockr_id', 'contraceptivestockr_id'])

        # Adding M2M table for field direct_indiv_sources on 'AggContraceptiveStockR'
        m2m_table_name = db.shorten_name(u'snisi_reprohealth_aggcontraceptivestockr_direct_indiv_sources')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('aggcontraceptivestockr', models.ForeignKey(orm[u'snisi_reprohealth.aggcontraceptivestockr'], null=False)),
            ('contraceptivestockr', models.ForeignKey(orm[u'snisi_reprohealth.contraceptivestockr'], null=False))
        ))
        db.create_unique(m2m_table_name, ['aggcontraceptivestockr_id', 'contraceptivestockr_id'])


    def backwards(self, orm):
        # Deleting model 'ProvidedServicesR'
        db.delete_table(u'snisi_reprohealth_providedservicesr')

        # Deleting model 'AggProvidedServicesR'
        db.delete_table(u'snisi_reprohealth_aggprovidedservicesr')

        # Removing M2M table for field agg_sources on 'AggProvidedServicesR'
        db.delete_table(db.shorten_name(u'snisi_reprohealth_aggprovidedservicesr_agg_sources'))

        # Removing M2M table for field direct_agg_sources on 'AggProvidedServicesR'
        db.delete_table(db.shorten_name(u'snisi_reprohealth_aggprovidedservicesr_direct_agg_sources'))

        # Removing M2M table for field indiv_sources on 'AggProvidedServicesR'
        db.delete_table(db.shorten_name(u'snisi_reprohealth_aggprovidedservicesr_indiv_sources'))

        # Removing M2M table for field direct_indiv_sources on 'AggProvidedServicesR'
        db.delete_table(db.shorten_name(u'snisi_reprohealth_aggprovidedservicesr_direct_indiv_sources'))

        # Deleting model 'FinancialR'
        db.delete_table(u'snisi_reprohealth_financialr')

        # Deleting model 'AggFinancialR'
        db.delete_table(u'snisi_reprohealth_aggfinancialr')

        # Removing M2M table for field agg_sources on 'AggFinancialR'
        db.delete_table(db.shorten_name(u'snisi_reprohealth_aggfinancialr_agg_sources'))

        # Removing M2M table for field direct_agg_sources on 'AggFinancialR'
        db.delete_table(db.shorten_name(u'snisi_reprohealth_aggfinancialr_direct_agg_sources'))

        # Removing M2M table for field indiv_sources on 'AggFinancialR'
        db.delete_table(db.shorten_name(u'snisi_reprohealth_aggfinancialr_indiv_sources'))

        # Removing M2M table for field direct_indiv_sources on 'AggFinancialR'
        db.delete_table(db.shorten_name(u'snisi_reprohealth_aggfinancialr_direct_indiv_sources'))

        # Deleting model 'ContraceptiveStockR'
        db.delete_table(u'snisi_reprohealth_contraceptivestockr')

        # Deleting model 'AggContraceptiveStockR'
        db.delete_table(u'snisi_reprohealth_aggcontraceptivestockr')

        # Removing M2M table for field agg_sources on 'AggContraceptiveStockR'
        db.delete_table(db.shorten_name(u'snisi_reprohealth_aggcontraceptivestockr_agg_sources'))

        # Removing M2M table for field direct_agg_sources on 'AggContraceptiveStockR'
        db.delete_table(db.shorten_name(u'snisi_reprohealth_aggcontraceptivestockr_direct_agg_sources'))

        # Removing M2M table for field indiv_sources on 'AggContraceptiveStockR'
        db.delete_table(db.shorten_name(u'snisi_reprohealth_aggcontraceptivestockr_indiv_sources'))

        # Removing M2M table for field direct_indiv_sources on 'AggContraceptiveStockR'
        db.delete_table(db.shorten_name(u'snisi_reprohealth_aggcontraceptivestockr_direct_indiv_sources'))


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
            'uuid': ('django.db.models.fields.CharField', [], {'default': "'6d17f22d-4f8f-4619-87c1-6448e04a778f'", 'max_length': '200', 'primary_key': 'True'}),
            'validated_by': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "u'own_validated_reports'", 'null': 'True', 'to': u"orm['snisi_core.Provider']"}),
            'validated_on': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'validation_status': ('django.db.models.fields.CharField', [], {'default': "u'not_applicable'", 'max_length': '40'})
        },
        u'snisi_reprohealth.aggcontraceptivestockr': {
            'Meta': {'object_name': 'AggContraceptiveStockR', '_ormbases': [u'snisi_core.SNISIReport']},
            'agg_sources': ('django.db.models.fields.related.ManyToManyField', [], {'blank': 'True', 'related_name': "u'aggregated_agg_aggcontraceptivestockr_reports'", 'null': 'True', 'symmetrical': 'False', 'to': u"orm['snisi_reprohealth.AggContraceptiveStockR']"}),
            'direct_agg_sources': ('django.db.models.fields.related.ManyToManyField', [], {'blank': 'True', 'related_name': "u'direct_aggregated_agg_aggcontraceptivestockr_reports'", 'null': 'True', 'symmetrical': 'False', 'to': u"orm['snisi_reprohealth.AggContraceptiveStockR']"}),
            'direct_indiv_sources': ('django.db.models.fields.related.ManyToManyField', [], {'blank': 'True', 'related_name': "u'direct_source_agg_aggcontraceptivestockr_reports'", 'null': 'True', 'symmetrical': 'False', 'to': u"orm['snisi_reprohealth.ContraceptiveStockR']"}),
            'female_condoms_initial': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'female_condoms_received': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'female_condoms_used': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'hiv_tests_initial': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'hiv_tests_received': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'hiv_tests_used': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'implants_initial': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'implants_received': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'implants_used': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'indiv_sources': ('django.db.models.fields.related.ManyToManyField', [], {'blank': 'True', 'related_name': "u'source_agg_aggcontraceptivestockr_reports'", 'null': 'True', 'symmetrical': 'False', 'to': u"orm['snisi_reprohealth.ContraceptiveStockR']"}),
            'injections_initial': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'injections_received': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'injections_used': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'intrauterine_devices_initial': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'intrauterine_devices_received': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'intrauterine_devices_used': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'male_condoms_initial': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'male_condoms_received': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'male_condoms_used': ('django.db.models.fields.PositiveIntegerField', [], {}),
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
            'pills_initial': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'pills_received': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'pills_used': ('django.db.models.fields.PositiveIntegerField', [], {}),
            u'snisireport_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['snisi_core.SNISIReport']", 'unique': 'True', 'primary_key': 'True'})
        },
        u'snisi_reprohealth.aggfinancialr': {
            'Meta': {'object_name': 'AggFinancialR', '_ormbases': [u'snisi_core.SNISIReport']},
            'agg_sources': ('django.db.models.fields.related.ManyToManyField', [], {'blank': 'True', 'related_name': "u'aggregated_agg_aggfinancialr_reports'", 'null': 'True', 'symmetrical': 'False', 'to': u"orm['snisi_reprohealth.AggFinancialR']"}),
            'direct_agg_sources': ('django.db.models.fields.related.ManyToManyField', [], {'blank': 'True', 'related_name': "u'direct_aggregated_agg_aggfinancialr_reports'", 'null': 'True', 'symmetrical': 'False', 'to': u"orm['snisi_reprohealth.AggFinancialR']"}),
            'direct_indiv_sources': ('django.db.models.fields.related.ManyToManyField', [], {'blank': 'True', 'related_name': "u'direct_source_agg_aggfinancialr_reports'", 'null': 'True', 'symmetrical': 'False', 'to': u"orm['snisi_reprohealth.FinancialR']"}),
            'female_condoms_price': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'female_condoms_qty': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'female_condoms_revenue': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'hiv_tests_price': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'hiv_tests_qty': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'hiv_tests_revenue': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'implant_removal_price': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'implant_removal_qty': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'implant_removal_revenue': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'implants_price': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'implants_qty': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'implants_revenue': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'indiv_sources': ('django.db.models.fields.related.ManyToManyField', [], {'blank': 'True', 'related_name': "u'source_agg_aggfinancialr_reports'", 'null': 'True', 'symmetrical': 'False', 'to': u"orm['snisi_reprohealth.FinancialR']"}),
            'injections_price': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'injections_qty': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'injections_revenue': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'intrauterine_devices_price': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'intrauterine_devices_qty': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'intrauterine_devices_revenue': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'iud_removal_price': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'iud_removal_qty': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'iud_removal_revenue': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'male_condoms_price': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'male_condoms_qty': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'male_condoms_revenue': ('django.db.models.fields.PositiveIntegerField', [], {}),
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
            'pills_price': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'pills_qty': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'pills_revenue': ('django.db.models.fields.PositiveIntegerField', [], {}),
            u'snisireport_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['snisi_core.SNISIReport']", 'unique': 'True', 'primary_key': 'True'})
        },
        u'snisi_reprohealth.aggprovidedservicesr': {
            'Meta': {'object_name': 'AggProvidedServicesR', '_ormbases': [u'snisi_core.SNISIReport']},
            'agg_sources': ('django.db.models.fields.related.ManyToManyField', [], {'blank': 'True', 'related_name': "u'aggregated_agg_aggprovidedservicesr_reports'", 'null': 'True', 'symmetrical': 'False', 'to': u"orm['snisi_reprohealth.AggProvidedServicesR']"}),
            'direct_agg_sources': ('django.db.models.fields.related.ManyToManyField', [], {'blank': 'True', 'related_name': "u'direct_aggregated_agg_aggprovidedservicesr_reports'", 'null': 'True', 'symmetrical': 'False', 'to': u"orm['snisi_reprohealth.AggProvidedServicesR']"}),
            'direct_indiv_sources': ('django.db.models.fields.related.ManyToManyField', [], {'blank': 'True', 'related_name': "u'direct_source_agg_aggprovidedservicesr_reports'", 'null': 'True', 'symmetrical': 'False', 'to': u"orm['snisi_reprohealth.ProvidedServicesR']"}),
            'emergency_controls': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'female_condoms': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'hiv_counseling_clients': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'hiv_positive_results': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'hiv_tests': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'implant_removals': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'implants': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'indiv_sources': ('django.db.models.fields.related.ManyToManyField', [], {'blank': 'True', 'related_name': "u'source_agg_aggprovidedservicesr_reports'", 'null': 'True', 'symmetrical': 'False', 'to': u"orm['snisi_reprohealth.ProvidedServicesR']"}),
            'injections': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'intrauterine_devices': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'iud_removal': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'long_term_method_visits': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'male_condoms': ('django.db.models.fields.PositiveIntegerField', [], {}),
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
            'new_clients': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'over25_visits': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'pills': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'previous_clients': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'short_term_method_visits': ('django.db.models.fields.PositiveIntegerField', [], {}),
            u'snisireport_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['snisi_core.SNISIReport']", 'unique': 'True', 'primary_key': 'True'}),
            'tubal_ligations': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'under25_visits': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'very_first_visits': ('django.db.models.fields.PositiveIntegerField', [], {})
        },
        u'snisi_reprohealth.contraceptivestockr': {
            'Meta': {'object_name': 'ContraceptiveStockR', '_ormbases': [u'snisi_core.SNISIReport']},
            'female_condoms_initial': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'female_condoms_observation': ('django.db.models.fields.CharField', [], {'max_length': '500', 'null': 'True', 'blank': 'True'}),
            'female_condoms_received': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'female_condoms_used': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'hiv_tests_initial': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'hiv_tests_observation': ('django.db.models.fields.CharField', [], {'max_length': '500', 'null': 'True', 'blank': 'True'}),
            'hiv_tests_received': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'hiv_tests_used': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'implants_initial': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'implants_observation': ('django.db.models.fields.CharField', [], {'max_length': '500', 'null': 'True', 'blank': 'True'}),
            'implants_received': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'implants_used': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'injections_initial': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'injections_observation': ('django.db.models.fields.CharField', [], {'max_length': '500', 'null': 'True', 'blank': 'True'}),
            'injections_received': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'injections_used': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'intrauterine_devices_initial': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'intrauterine_devices_observation': ('django.db.models.fields.CharField', [], {'max_length': '500', 'null': 'True', 'blank': 'True'}),
            'intrauterine_devices_received': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'intrauterine_devices_used': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'male_condoms_initial': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'male_condoms_observation': ('django.db.models.fields.CharField', [], {'max_length': '500', 'null': 'True', 'blank': 'True'}),
            'male_condoms_received': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'male_condoms_used': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'pills_initial': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'pills_observation': ('django.db.models.fields.CharField', [], {'max_length': '500', 'null': 'True', 'blank': 'True'}),
            'pills_received': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'pills_used': ('django.db.models.fields.PositiveIntegerField', [], {}),
            u'snisireport_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['snisi_core.SNISIReport']", 'unique': 'True', 'primary_key': 'True'})
        },
        u'snisi_reprohealth.financialr': {
            'Meta': {'object_name': 'FinancialR', '_ormbases': [u'snisi_core.SNISIReport']},
            'female_condoms_price': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'female_condoms_qty': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'female_condoms_revenue': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'hiv_tests_price': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'hiv_tests_qty': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'hiv_tests_revenue': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'implant_removal_price': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'implant_removal_qty': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'implant_removal_revenue': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'implants_price': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'implants_qty': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'implants_revenue': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'injections_price': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'injections_qty': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'injections_revenue': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'intrauterine_devices_price': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'intrauterine_devices_qty': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'intrauterine_devices_revenue': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'iud_removal_price': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'iud_removal_qty': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'iud_removal_revenue': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'male_condoms_price': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'male_condoms_qty': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'male_condoms_revenue': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'pills_price': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'pills_qty': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'pills_revenue': ('django.db.models.fields.PositiveIntegerField', [], {}),
            u'snisireport_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['snisi_core.SNISIReport']", 'unique': 'True', 'primary_key': 'True'})
        },
        u'snisi_reprohealth.providedservicesr': {
            'Meta': {'object_name': 'ProvidedServicesR', '_ormbases': [u'snisi_core.SNISIReport']},
            'emergency_controls': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'female_condoms': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'hiv_counseling_clients': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'hiv_positive_results': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'hiv_tests': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'implant_removals': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'implants': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'injections': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'intrauterine_devices': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'iud_removal': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'long_term_method_visits': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'male_condoms': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'new_clients': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'over25_visits': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'pills': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'previous_clients': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'short_term_method_visits': ('django.db.models.fields.PositiveIntegerField', [], {}),
            u'snisireport_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['snisi_core.SNISIReport']", 'unique': 'True', 'primary_key': 'True'}),
            'tubal_ligations': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'under25_visits': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'very_first_visits': ('django.db.models.fields.PositiveIntegerField', [], {})
        }
    }

    complete_apps = ['snisi_reprohealth']