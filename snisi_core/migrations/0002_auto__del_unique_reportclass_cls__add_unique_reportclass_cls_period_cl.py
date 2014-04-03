# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Removing unique constraint on 'ReportClass', fields ['cls']
        db.delete_unique(u'snisi_core_reportclass', ['cls'])

        # Adding unique constraint on 'ReportClass', fields ['cls', 'period_cls', 'report_type']
        db.create_unique(u'snisi_core_reportclass', ['cls', 'period_cls', 'report_type'])


    def backwards(self, orm):
        # Removing unique constraint on 'ReportClass', fields ['cls', 'period_cls', 'report_type']
        db.delete_unique(u'snisi_core_reportclass', ['cls', 'period_cls', 'report_type'])

        # Adding unique constraint on 'ReportClass', fields ['cls']
        db.create_unique(u'snisi_core_reportclass', ['cls'])


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
        u'snisi_core.administrativeentity': {
            'Meta': {'object_name': 'AdministrativeEntity', '_ormbases': [u'snisi_core.Entity']},
            u'entity_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['snisi_core.Entity']", 'unique': 'True', 'primary_key': 'True'}),
            'health_entity': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "u'admin_entities'", 'null': 'True', 'to': u"orm['snisi_core.HealthEntity']"}),
            'main_entity_distance': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'})
        },
        u'snisi_core.cluster': {
            'Meta': {'object_name': 'Cluster'},
            'contact': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "u'clusters_as_contact'", 'null': 'True', 'to': u"orm['snisi_core.Provider']"}),
            'domain': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['snisi_core.Domain']", 'null': 'True', 'blank': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '250'}),
            'slug': ('django.db.models.fields.CharField', [], {'max_length': '75', 'primary_key': 'True'})
        },
        u'snisi_core.domain': {
            'Meta': {'object_name': 'Domain'},
            'description': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'module_path': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '200'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '250'}),
            'operational_contact': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "u'projects_as_opcontact'", 'null': 'True', 'to': u"orm['snisi_core.Provider']"}),
            'short_description': ('django.db.models.fields.CharField', [], {'max_length': '250', 'null': 'True', 'blank': 'True'}),
            'slug': ('django.db.models.fields.CharField', [], {'max_length': '75', 'primary_key': 'True'}),
            'technical_contact': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "u'projects_as_techcontact'", 'null': 'True', 'to': u"orm['snisi_core.Provider']"})
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
        u'snisi_core.expectedreporting': {
            'Meta': {'object_name': 'ExpectedReporting'},
            'amount_expected': ('django.db.models.fields.CharField', [], {'max_length': '30'}),
            'arrived_reports': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': u"orm['snisi_core.SNISIReport']", 'null': 'True', 'blank': 'True'}),
            'completion_status': ('django.db.models.fields.CharField', [], {'max_length': '30'}),
            'entity': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['snisi_core.Entity']"}),
            'extended_reporting_period': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "u'expr_for_ext_reporting_period'", 'null': 'True', 'to': u"orm['snisi_core.Period']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'period': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "u'expr_for_period'", 'to': u"orm['snisi_core.Period']"}),
            'report_class': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['snisi_core.ReportClass']"}),
            'reporting_period': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "u'expr_for_reporting_period'", 'null': 'True', 'to': u"orm['snisi_core.Period']"}),
            'reporting_role': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['snisi_core.Role']", 'null': 'True', 'blank': 'True'}),
            'updated_on': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'within_entity': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'within_period': ('django.db.models.fields.BooleanField', [], {})
        },
        u'snisi_core.expectedvalidation': {
            'Meta': {'object_name': 'ExpectedValidation'},
            'report': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "u'expected_validations'", 'primary_key': 'True', 'to': u"orm['snisi_core.SNISIReport']"}),
            'satisfied': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'validated_on': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'validating_entity': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['snisi_core.Entity']"}),
            'validating_role': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['snisi_core.Role']"}),
            'validation_period': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['snisi_core.Period']"})
        },
        u'snisi_core.healthentity': {
            'Meta': {'object_name': 'HealthEntity', '_ormbases': [u'snisi_core.Entity']},
            u'entity_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['snisi_core.Entity']", 'unique': 'True', 'primary_key': 'True'}),
            'main_entity': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['snisi_core.HealthEntity']", 'null': 'True', 'blank': 'True'})
        },
        u'snisi_core.notification': {
            'Meta': {'object_name': 'Notification'},
            'category': ('django.db.models.fields.CharField', [], {'max_length': '75', 'null': 'True', 'blank': 'True'}),
            'created_on': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'deliver': ('django.db.models.fields.CharField', [], {'max_length': '75'}),
            'delivery_status': ('django.db.models.fields.CharField', [], {'default': "u'unknown'", 'max_length': '75'}),
            'destination_email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'null': 'True', 'blank': 'True'}),
            'destination_number': ('django.db.models.fields.CharField', [], {'max_length': '75', 'null': 'True', 'blank': 'True'}),
            'expirate_on': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'important': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'level': ('django.db.models.fields.CharField', [], {'default': "u'info'", 'max_length': '75'}),
            'method': ('django.db.models.fields.CharField', [], {'default': "u'preferred'", 'max_length': '75'}),
            'provider': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['snisi_core.Provider']", 'null': 'True', 'blank': 'True'}),
            'sent': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'sent_on': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'text': ('django.db.models.fields.TextField', [], {}),
            'text_short': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'title': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'})
        },
        u'snisi_core.participation': {
            'Meta': {'unique_together': "[(u'cluster', u'entity')]", 'object_name': 'Participation'},
            'cluster': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "u'participations'", 'to': u"orm['snisi_core.Cluster']"}),
            'entity': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "u'participations'", 'to': u"orm['snisi_core.Entity']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'modified_on': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'})
        },
        u'snisi_core.period': {
            'Meta': {'unique_together': "((u'start_on', u'end_on', u'period_type'),)", 'object_name': 'Period'},
            'end_on': ('django.db.models.fields.DateTimeField', [], {}),
            'identifier': ('django.db.models.fields.CharField', [], {'max_length': '200', 'primary_key': 'True'}),
            'period_type': ('django.db.models.fields.CharField', [], {'default': "u'custom'", 'max_length': '100'}),
            'start_on': ('django.db.models.fields.DateTimeField', [], {})
        },
        u'snisi_core.phonenumber': {
            'Meta': {'ordering': "(u'provider', u'-priority')", 'object_name': 'PhoneNumber'},
            'category': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['snisi_core.PhoneNumberType']"}),
            'identity': ('django.db.models.fields.CharField', [], {'max_length': '75', 'primary_key': 'True'}),
            'priority': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'}),
            'provider': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "u'phone_numbers'", 'to': u"orm['snisi_core.Provider']"})
        },
        u'snisi_core.phonenumbertype': {
            'Meta': {'ordering': "(u'name',)", 'object_name': 'PhoneNumberType'},
            'abbr': ('django.db.models.fields.CharField', [], {'max_length': '10'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'priority': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'}),
            'slug': ('django.db.models.fields.CharField', [], {'max_length': '75', 'primary_key': 'True'})
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
        u'snisi_core.reportclass': {
            'Meta': {'unique_together': "[(u'cls', u'period_cls', u'report_type')]", 'object_name': 'ReportClass'},
            'cls': ('django.db.models.fields.CharField', [], {'max_length': '75'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '150'}),
            'period_cls': ('django.db.models.fields.CharField', [], {'max_length': '75'}),
            'report_type': ('django.db.models.fields.CharField', [], {'max_length': '30'}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '75', 'primary_key': 'True'})
        },
        u'snisi_core.role': {
            'Meta': {'object_name': 'Role'},
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '15', 'primary_key': 'True'})
        },
        u'snisi_core.smsmessage': {
            'Meta': {'object_name': 'SMSMessage'},
            'created_on': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'deferred': ('django.db.models.fields.PositiveIntegerField', [], {'null': 'True', 'blank': 'True'}),
            'delivery_status': ('django.db.models.fields.CharField', [], {'default': "u'unknown'", 'max_length': '75'}),
            'direction': ('django.db.models.fields.CharField', [], {'max_length': '75'}),
            'event_on': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'handled': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'identity': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'text': ('django.db.models.fields.TextField', [], {}),
            'validity': ('django.db.models.fields.PositiveIntegerField', [], {'null': 'True', 'blank': 'True'})
        },
        u'snisi_core.snisigroup': {
            'Meta': {'object_name': 'SNISIGroup', '_ormbases': [u'auth.Group']},
            u'group_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['auth.Group']", 'unique': 'True', 'primary_key': 'True'})
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
            'uuid': ('django.db.models.fields.CharField', [], {'default': "'3b9f0f2d-8ce0-49bf-abc4-e07500fb7a07'", 'max_length': '200', 'primary_key': 'True'}),
            'validated_by': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "u'own_validated_reports'", 'null': 'True', 'to': u"orm['snisi_core.Provider']"}),
            'validated_on': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'validation_status': ('django.db.models.fields.CharField', [], {'default': "u'not_applicable'", 'max_length': '40'})
        }
    }

    complete_apps = ['snisi_core']