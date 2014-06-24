# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'VaccCovR'
        db.create_table(u'snisi_vacc_vacccovr', (
            (u'snisireport_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['snisi_core.SNISIReport'], unique=True, primary_key=True)),
            ('bcg_coverage', self.gf('django.db.models.fields.FloatField')()),
            ('polio3_coverage', self.gf('django.db.models.fields.FloatField')()),
            ('measles_coverage', self.gf('django.db.models.fields.FloatField')()),
            ('polio3_abandonment_rate', self.gf('django.db.models.fields.FloatField')()),
        ))
        db.send_create_signal(u'snisi_vacc', ['VaccCovR'])

        # Adding model 'AggVaccCovR'
        db.create_table(u'snisi_vacc_aggvacccovr', (
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
            ('bcg_coverage', self.gf('django.db.models.fields.FloatField')()),
            ('polio3_coverage', self.gf('django.db.models.fields.FloatField')()),
            ('measles_coverage', self.gf('django.db.models.fields.FloatField')()),
            ('polio3_abandonment_rate', self.gf('django.db.models.fields.FloatField')()),
        ))
        db.send_create_signal(u'snisi_vacc', ['AggVaccCovR'])

        # Adding M2M table for field agg_sources on 'AggVaccCovR'
        m2m_table_name = db.shorten_name(u'snisi_vacc_aggvacccovr_agg_sources')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('from_aggvacccovr', models.ForeignKey(orm[u'snisi_vacc.aggvacccovr'], null=False)),
            ('to_aggvacccovr', models.ForeignKey(orm[u'snisi_vacc.aggvacccovr'], null=False))
        ))
        db.create_unique(m2m_table_name, ['from_aggvacccovr_id', 'to_aggvacccovr_id'])

        # Adding M2M table for field direct_agg_sources on 'AggVaccCovR'
        m2m_table_name = db.shorten_name(u'snisi_vacc_aggvacccovr_direct_agg_sources')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('from_aggvacccovr', models.ForeignKey(orm[u'snisi_vacc.aggvacccovr'], null=False)),
            ('to_aggvacccovr', models.ForeignKey(orm[u'snisi_vacc.aggvacccovr'], null=False))
        ))
        db.create_unique(m2m_table_name, ['from_aggvacccovr_id', 'to_aggvacccovr_id'])

        # Adding M2M table for field indiv_sources on 'AggVaccCovR'
        m2m_table_name = db.shorten_name(u'snisi_vacc_aggvacccovr_indiv_sources')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('aggvacccovr', models.ForeignKey(orm[u'snisi_vacc.aggvacccovr'], null=False)),
            ('vacccovr', models.ForeignKey(orm[u'snisi_vacc.vacccovr'], null=False))
        ))
        db.create_unique(m2m_table_name, ['aggvacccovr_id', 'vacccovr_id'])

        # Adding M2M table for field direct_indiv_sources on 'AggVaccCovR'
        m2m_table_name = db.shorten_name(u'snisi_vacc_aggvacccovr_direct_indiv_sources')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('aggvacccovr', models.ForeignKey(orm[u'snisi_vacc.aggvacccovr'], null=False)),
            ('vacccovr', models.ForeignKey(orm[u'snisi_vacc.vacccovr'], null=False))
        ))
        db.create_unique(m2m_table_name, ['aggvacccovr_id', 'vacccovr_id'])


    def backwards(self, orm):
        # Deleting model 'VaccCovR'
        db.delete_table(u'snisi_vacc_vacccovr')

        # Deleting model 'AggVaccCovR'
        db.delete_table(u'snisi_vacc_aggvacccovr')

        # Removing M2M table for field agg_sources on 'AggVaccCovR'
        db.delete_table(db.shorten_name(u'snisi_vacc_aggvacccovr_agg_sources'))

        # Removing M2M table for field direct_agg_sources on 'AggVaccCovR'
        db.delete_table(db.shorten_name(u'snisi_vacc_aggvacccovr_direct_agg_sources'))

        # Removing M2M table for field indiv_sources on 'AggVaccCovR'
        db.delete_table(db.shorten_name(u'snisi_vacc_aggvacccovr_indiv_sources'))

        # Removing M2M table for field direct_indiv_sources on 'AggVaccCovR'
        db.delete_table(db.shorten_name(u'snisi_vacc_aggvacccovr_direct_indiv_sources'))


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
            'uuid': ('django.db.models.fields.CharField', [], {'default': "'b9c82a10-e676-4b63-8c4e-41397e4dc1a1'", 'max_length': '200', 'primary_key': 'True'}),
            'validated_by': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "u'own_validated_reports'", 'null': 'True', 'to': u"orm['snisi_core.Provider']"}),
            'validated_on': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'validation_status': ('django.db.models.fields.CharField', [], {'default': "u'not_applicable'", 'max_length': '40'})
        },
        u'snisi_vacc.aggvacccovr': {
            'Meta': {'object_name': 'AggVaccCovR', '_ormbases': [u'snisi_core.SNISIReport']},
            'agg_sources': ('django.db.models.fields.related.ManyToManyField', [], {'blank': 'True', 'related_name': "u'aggregated_agg_aggvacccovr_reports'", 'null': 'True', 'symmetrical': 'False', 'to': u"orm['snisi_vacc.AggVaccCovR']"}),
            'bcg_coverage': ('django.db.models.fields.FloatField', [], {}),
            'direct_agg_sources': ('django.db.models.fields.related.ManyToManyField', [], {'blank': 'True', 'related_name': "u'direct_aggregated_agg_aggvacccovr_reports'", 'null': 'True', 'symmetrical': 'False', 'to': u"orm['snisi_vacc.AggVaccCovR']"}),
            'direct_indiv_sources': ('django.db.models.fields.related.ManyToManyField', [], {'blank': 'True', 'related_name': "u'direct_source_agg_aggvacccovr_reports'", 'null': 'True', 'symmetrical': 'False', 'to': u"orm['snisi_vacc.VaccCovR']"}),
            'indiv_sources': ('django.db.models.fields.related.ManyToManyField', [], {'blank': 'True', 'related_name': "u'source_agg_aggvacccovr_reports'", 'null': 'True', 'symmetrical': 'False', 'to': u"orm['snisi_vacc.VaccCovR']"}),
            'measles_coverage': ('django.db.models.fields.FloatField', [], {}),
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
            'polio3_abandonment_rate': ('django.db.models.fields.FloatField', [], {}),
            'polio3_coverage': ('django.db.models.fields.FloatField', [], {}),
            u'snisireport_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['snisi_core.SNISIReport']", 'unique': 'True', 'primary_key': 'True'})
        },
        u'snisi_vacc.vacccovr': {
            'Meta': {'object_name': 'VaccCovR', '_ormbases': [u'snisi_core.SNISIReport']},
            'bcg_coverage': ('django.db.models.fields.FloatField', [], {}),
            'measles_coverage': ('django.db.models.fields.FloatField', [], {}),
            'polio3_abandonment_rate': ('django.db.models.fields.FloatField', [], {}),
            'polio3_coverage': ('django.db.models.fields.FloatField', [], {}),
            u'snisireport_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['snisi_core.SNISIReport']", 'unique': 'True', 'primary_key': 'True'})
        }
    }

    complete_apps = ['snisi_vacc']