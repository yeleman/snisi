# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'AggTTBacklogMissionR.nb_days_total'
        db.add_column(u'snisi_trachoma_aggttbacklogmissionr', 'nb_days_total',
                      self.gf('django.db.models.fields.PositiveIntegerField')(default=0),
                      keep_default=False)

        # Adding field 'TTBacklogMissionR.nb_days_total'
        db.add_column(u'snisi_trachoma_ttbacklogmissionr', 'nb_days_total',
                      self.gf('django.db.models.fields.PositiveIntegerField')(default=0),
                      keep_default=False)


    def backwards(self, orm):
        # Deleting field 'AggTTBacklogMissionR.nb_days_total'
        db.delete_column(u'snisi_trachoma_aggttbacklogmissionr', 'nb_days_total')

        # Deleting field 'TTBacklogMissionR.nb_days_total'
        db.delete_column(u'snisi_trachoma_ttbacklogmissionr', 'nb_days_total')


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
            'uuid': ('django.db.models.fields.CharField', [], {'default': "'26a62839-ddb6-409b-9fe8-fc471f87cd03'", 'max_length': '200', 'primary_key': 'True'}),
            'validated_by': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "u'own_validated_reports'", 'null': 'True', 'to': u"orm['snisi_core.Provider']"}),
            'validated_on': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'validation_status': ('django.db.models.fields.CharField', [], {'default': "u'not_applicable'", 'max_length': '40'})
        },
        u'snisi_trachoma.aggttbacklogmissionr': {
            'Meta': {'object_name': 'AggTTBacklogMissionR', '_ormbases': [u'snisi_core.SNISIReport']},
            'agg_sources': ('django.db.models.fields.related.ManyToManyField', [], {'blank': 'True', 'related_name': "u'aggregated_agg_aggttbacklogmissionr_reports'", 'null': 'True', 'symmetrical': 'False', 'to': u"orm['snisi_trachoma.AggTTBacklogMissionR']"}),
            'community_assistance': ('django.db.models.fields.BooleanField', [], {}),
            'consultation_female': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'consultation_male': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'direct_agg_sources': ('django.db.models.fields.related.ManyToManyField', [], {'blank': 'True', 'related_name': "u'direct_aggregated_agg_aggttbacklogmissionr_reports'", 'null': 'True', 'symmetrical': 'False', 'to': u"orm['snisi_trachoma.AggTTBacklogMissionR']"}),
            'nb_agg_reports_altered': ('django.db.models.fields.PositiveIntegerField', [], {'null': 'True', 'blank': 'True'}),
            'nb_agg_reports_auto_validated': ('django.db.models.fields.PositiveIntegerField', [], {'null': 'True', 'blank': 'True'}),
            'nb_agg_reports_validated': ('django.db.models.fields.PositiveIntegerField', [], {'null': 'True', 'blank': 'True'}),
            'nb_community_assistance': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'nb_days_avg': ('django.db.models.fields.FloatField', [], {}),
            'nb_days_max': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'nb_days_med': ('django.db.models.fields.FloatField', [], {}),
            'nb_days_min': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'nb_days_total': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'nb_source_reports_altered': ('django.db.models.fields.PositiveIntegerField', [], {'null': 'True', 'blank': 'True'}),
            'nb_source_reports_arrived': ('django.db.models.fields.PositiveIntegerField', [], {'null': 'True', 'blank': 'True'}),
            'nb_source_reports_arrived_complete': ('django.db.models.fields.PositiveIntegerField', [], {'null': 'True', 'blank': 'True'}),
            'nb_source_reports_arrived_correct': ('django.db.models.fields.PositiveIntegerField', [], {'null': 'True', 'blank': 'True'}),
            'nb_source_reports_arrived_on_time': ('django.db.models.fields.PositiveIntegerField', [], {'null': 'True', 'blank': 'True'}),
            'nb_source_reports_auto_validated': ('django.db.models.fields.PositiveIntegerField', [], {'null': 'True', 'blank': 'True'}),
            'nb_source_reports_expected': ('django.db.models.fields.PositiveIntegerField', [], {'null': 'True', 'blank': 'True'}),
            'nb_source_reports_validated': ('django.db.models.fields.PositiveIntegerField', [], {'null': 'True', 'blank': 'True'}),
            'nb_village_reports': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'recidivism_female': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'recidivism_male': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'refusal_female': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'refusal_male': ('django.db.models.fields.PositiveIntegerField', [], {}),
            u'snisireport_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['snisi_core.SNISIReport']", 'unique': 'True', 'primary_key': 'True'}),
            'surgery_female': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'surgery_male': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'village_reports': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': u"orm['snisi_trachoma.TTBacklogVillageR']", 'null': 'True', 'blank': 'True'})
        },
        u'snisi_trachoma.ttbacklogmissionr': {
            'Meta': {'object_name': 'TTBacklogMissionR', '_ormbases': [u'snisi_core.SNISIReport']},
            'community_assistance': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'consultation_female': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'}),
            'consultation_male': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'}),
            'ended_on': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'nb_community_assistance': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'}),
            'nb_days_max': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'}),
            'nb_days_mean': ('django.db.models.fields.FloatField', [], {'default': '0'}),
            'nb_days_median': ('django.db.models.fields.FloatField', [], {'default': '0'}),
            'nb_days_min': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'}),
            'nb_days_total': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'}),
            'nb_village_reports': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'}),
            'operator': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['snisi_core.Provider']"}),
            'operator_type': ('django.db.models.fields.CharField', [], {'max_length': '75'}),
            'recidivism_female': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'}),
            'recidivism_male': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'}),
            'refusal_female': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'}),
            'refusal_male': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'}),
            u'snisireport_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['snisi_core.SNISIReport']", 'unique': 'True', 'primary_key': 'True'}),
            'started_on': ('django.db.models.fields.DateField', [], {}),
            'strategy': ('django.db.models.fields.CharField', [], {'max_length': '75'}),
            'surgery_female': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'}),
            'surgery_male': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'}),
            'village_reports': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': u"orm['snisi_trachoma.TTBacklogVillageR']", 'null': 'True', 'blank': 'True'})
        },
        u'snisi_trachoma.ttbacklogvillager': {
            'Meta': {'object_name': 'TTBacklogVillageR', '_ormbases': [u'snisi_core.SNISIReport']},
            'arrived_on': ('django.db.models.fields.DateField', [], {}),
            'community_assistance': ('django.db.models.fields.BooleanField', [], {}),
            'consultation_female': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'consultation_male': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'left_on': ('django.db.models.fields.DateField', [], {}),
            'location': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['snisi_core.Entity']"}),
            'recidivism_female': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'recidivism_male': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'refusal_female': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'refusal_male': ('django.db.models.fields.PositiveIntegerField', [], {}),
            u'snisireport_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['snisi_core.SNISIReport']", 'unique': 'True', 'primary_key': 'True'}),
            'surgery_female': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'surgery_male': ('django.db.models.fields.PositiveIntegerField', [], {})
        }
    }

    complete_apps = ['snisi_trachoma']