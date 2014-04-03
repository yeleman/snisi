# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Deleting field 'EpidemioMalariaR.u5_total_ge_parasite_pf_malaria_cases'
        db.delete_column(u'snisi_malaria_epidemiomalariar', 'u5_total_ge_parasite_pf_malaria_cases')

        # Deleting field 'EpidemioMalariaR.u5_total_tdr_parasite_pf_malaria_cases'
        db.delete_column(u'snisi_malaria_epidemiomalariar', 'u5_total_tdr_parasite_pf_malaria_cases')

        # Deleting field 'EpidemioMalariaR.o5_total_tdr_confirmed_malaria_cases'
        db.delete_column(u'snisi_malaria_epidemiomalariar', 'o5_total_tdr_confirmed_malaria_cases')

        # Deleting field 'EpidemioMalariaR.o5_total_ge_tested_malaria_cases'
        db.delete_column(u'snisi_malaria_epidemiomalariar', 'o5_total_ge_tested_malaria_cases')

        # Deleting field 'EpidemioMalariaR.u5_total_ge_confirmed_malaria_cases'
        db.delete_column(u'snisi_malaria_epidemiomalariar', 'u5_total_ge_confirmed_malaria_cases')

        # Deleting field 'EpidemioMalariaR.u5_total_tdr_confirmed_malaria_cases'
        db.delete_column(u'snisi_malaria_epidemiomalariar', 'u5_total_tdr_confirmed_malaria_cases')

        # Deleting field 'EpidemioMalariaR.pw_total_ge_tested_malaria_cases'
        db.delete_column(u'snisi_malaria_epidemiomalariar', 'pw_total_ge_tested_malaria_cases')

        # Deleting field 'EpidemioMalariaR.u5_total_tdr_tested_malaria_cases'
        db.delete_column(u'snisi_malaria_epidemiomalariar', 'u5_total_tdr_tested_malaria_cases')

        # Deleting field 'EpidemioMalariaR.u5_total_ge_tested_malaria_cases'
        db.delete_column(u'snisi_malaria_epidemiomalariar', 'u5_total_ge_tested_malaria_cases')

        # Deleting field 'EpidemioMalariaR.pw_total_tdr_parasite_pf_malaria_cases'
        db.delete_column(u'snisi_malaria_epidemiomalariar', 'pw_total_tdr_parasite_pf_malaria_cases')

        # Deleting field 'EpidemioMalariaR.o5_total_tdr_tested_malaria_cases'
        db.delete_column(u'snisi_malaria_epidemiomalariar', 'o5_total_tdr_tested_malaria_cases')

        # Deleting field 'EpidemioMalariaR.pw_total_ge_confirmed_malaria_cases'
        db.delete_column(u'snisi_malaria_epidemiomalariar', 'pw_total_ge_confirmed_malaria_cases')

        # Deleting field 'EpidemioMalariaR.o5_total_tdr_parasite_pf_malaria_cases'
        db.delete_column(u'snisi_malaria_epidemiomalariar', 'o5_total_tdr_parasite_pf_malaria_cases')

        # Deleting field 'EpidemioMalariaR.o5_total_ge_confirmed_malaria_cases'
        db.delete_column(u'snisi_malaria_epidemiomalariar', 'o5_total_ge_confirmed_malaria_cases')

        # Deleting field 'EpidemioMalariaR.pw_total_ge_parasite_pf_malaria_cases'
        db.delete_column(u'snisi_malaria_epidemiomalariar', 'pw_total_ge_parasite_pf_malaria_cases')

        # Deleting field 'EpidemioMalariaR.pw_total_tdr_confirmed_malaria_cases'
        db.delete_column(u'snisi_malaria_epidemiomalariar', 'pw_total_tdr_confirmed_malaria_cases')

        # Deleting field 'EpidemioMalariaR.pw_total_tdr_tested_malaria_cases'
        db.delete_column(u'snisi_malaria_epidemiomalariar', 'pw_total_tdr_tested_malaria_cases')

        # Deleting field 'EpidemioMalariaR.o5_total_ge_parasite_pf_malaria_cases'
        db.delete_column(u'snisi_malaria_epidemiomalariar', 'o5_total_ge_parasite_pf_malaria_cases')

        # Adding field 'EpidemioMalariaR.u5_total_rdt_tested_malaria_cases'
        db.add_column(u'snisi_malaria_epidemiomalariar', 'u5_total_rdt_tested_malaria_cases',
                      self.gf('django.db.models.fields.PositiveIntegerField')(default=0),
                      keep_default=False)

        # Adding field 'EpidemioMalariaR.u5_total_rdt_confirmed_malaria_cases'
        db.add_column(u'snisi_malaria_epidemiomalariar', 'u5_total_rdt_confirmed_malaria_cases',
                      self.gf('django.db.models.fields.PositiveIntegerField')(default=0),
                      keep_default=False)

        # Adding field 'EpidemioMalariaR.u5_total_rdt_pfalciparum_malaria_cases'
        db.add_column(u'snisi_malaria_epidemiomalariar', 'u5_total_rdt_pfalciparum_malaria_cases',
                      self.gf('django.db.models.fields.PositiveIntegerField')(default=0),
                      keep_default=False)

        # Adding field 'EpidemioMalariaR.u5_total_ts_tested_malaria_cases'
        db.add_column(u'snisi_malaria_epidemiomalariar', 'u5_total_ts_tested_malaria_cases',
                      self.gf('django.db.models.fields.PositiveIntegerField')(default=0),
                      keep_default=False)

        # Adding field 'EpidemioMalariaR.u5_total_ts_confirmed_malaria_cases'
        db.add_column(u'snisi_malaria_epidemiomalariar', 'u5_total_ts_confirmed_malaria_cases',
                      self.gf('django.db.models.fields.PositiveIntegerField')(default=0),
                      keep_default=False)

        # Adding field 'EpidemioMalariaR.u5_total_ts_pfalciparum_malaria_cases'
        db.add_column(u'snisi_malaria_epidemiomalariar', 'u5_total_ts_pfalciparum_malaria_cases',
                      self.gf('django.db.models.fields.PositiveIntegerField')(default=0),
                      keep_default=False)

        # Adding field 'EpidemioMalariaR.o5_total_rdt_tested_malaria_cases'
        db.add_column(u'snisi_malaria_epidemiomalariar', 'o5_total_rdt_tested_malaria_cases',
                      self.gf('django.db.models.fields.PositiveIntegerField')(default=0),
                      keep_default=False)

        # Adding field 'EpidemioMalariaR.o5_total_rdt_confirmed_malaria_cases'
        db.add_column(u'snisi_malaria_epidemiomalariar', 'o5_total_rdt_confirmed_malaria_cases',
                      self.gf('django.db.models.fields.PositiveIntegerField')(default=0),
                      keep_default=False)

        # Adding field 'EpidemioMalariaR.o5_total_rdt_pfalciparum_malaria_cases'
        db.add_column(u'snisi_malaria_epidemiomalariar', 'o5_total_rdt_pfalciparum_malaria_cases',
                      self.gf('django.db.models.fields.PositiveIntegerField')(default=0),
                      keep_default=False)

        # Adding field 'EpidemioMalariaR.o5_total_ts_tested_malaria_cases'
        db.add_column(u'snisi_malaria_epidemiomalariar', 'o5_total_ts_tested_malaria_cases',
                      self.gf('django.db.models.fields.PositiveIntegerField')(default=0),
                      keep_default=False)

        # Adding field 'EpidemioMalariaR.o5_total_ts_confirmed_malaria_cases'
        db.add_column(u'snisi_malaria_epidemiomalariar', 'o5_total_ts_confirmed_malaria_cases',
                      self.gf('django.db.models.fields.PositiveIntegerField')(default=0),
                      keep_default=False)

        # Adding field 'EpidemioMalariaR.o5_total_ts_pfalciparum_malaria_cases'
        db.add_column(u'snisi_malaria_epidemiomalariar', 'o5_total_ts_pfalciparum_malaria_cases',
                      self.gf('django.db.models.fields.PositiveIntegerField')(default=0),
                      keep_default=False)

        # Adding field 'EpidemioMalariaR.pw_total_rdt_tested_malaria_cases'
        db.add_column(u'snisi_malaria_epidemiomalariar', 'pw_total_rdt_tested_malaria_cases',
                      self.gf('django.db.models.fields.PositiveIntegerField')(default=0),
                      keep_default=False)

        # Adding field 'EpidemioMalariaR.pw_total_rdt_confirmed_malaria_cases'
        db.add_column(u'snisi_malaria_epidemiomalariar', 'pw_total_rdt_confirmed_malaria_cases',
                      self.gf('django.db.models.fields.PositiveIntegerField')(default=0),
                      keep_default=False)

        # Adding field 'EpidemioMalariaR.pw_total_rdt_pfalciparum_malaria_cases'
        db.add_column(u'snisi_malaria_epidemiomalariar', 'pw_total_rdt_pfalciparum_malaria_cases',
                      self.gf('django.db.models.fields.PositiveIntegerField')(default=0),
                      keep_default=False)

        # Adding field 'EpidemioMalariaR.pw_total_ts_tested_malaria_cases'
        db.add_column(u'snisi_malaria_epidemiomalariar', 'pw_total_ts_tested_malaria_cases',
                      self.gf('django.db.models.fields.PositiveIntegerField')(default=0),
                      keep_default=False)

        # Adding field 'EpidemioMalariaR.pw_total_ts_confirmed_malaria_cases'
        db.add_column(u'snisi_malaria_epidemiomalariar', 'pw_total_ts_confirmed_malaria_cases',
                      self.gf('django.db.models.fields.PositiveIntegerField')(default=0),
                      keep_default=False)

        # Adding field 'EpidemioMalariaR.pw_total_ts_pfalciparum_malaria_cases'
        db.add_column(u'snisi_malaria_epidemiomalariar', 'pw_total_ts_pfalciparum_malaria_cases',
                      self.gf('django.db.models.fields.PositiveIntegerField')(default=0),
                      keep_default=False)

        # Deleting field 'AggEpidemioMalariaR.pw_total_ge_tested_malaria_cases'
        db.delete_column(u'snisi_malaria_aggepidemiomalariar', 'pw_total_ge_tested_malaria_cases')

        # Deleting field 'AggEpidemioMalariaR.pw_total_ge_confirmed_malaria_cases'
        db.delete_column(u'snisi_malaria_aggepidemiomalariar', 'pw_total_ge_confirmed_malaria_cases')

        # Deleting field 'AggEpidemioMalariaR.o5_total_tdr_tested_malaria_cases'
        db.delete_column(u'snisi_malaria_aggepidemiomalariar', 'o5_total_tdr_tested_malaria_cases')

        # Deleting field 'AggEpidemioMalariaR.u5_total_ge_tested_malaria_cases'
        db.delete_column(u'snisi_malaria_aggepidemiomalariar', 'u5_total_ge_tested_malaria_cases')

        # Deleting field 'AggEpidemioMalariaR.u5_total_ge_confirmed_malaria_cases'
        db.delete_column(u'snisi_malaria_aggepidemiomalariar', 'u5_total_ge_confirmed_malaria_cases')

        # Deleting field 'AggEpidemioMalariaR.o5_total_ge_tested_malaria_cases'
        db.delete_column(u'snisi_malaria_aggepidemiomalariar', 'o5_total_ge_tested_malaria_cases')

        # Deleting field 'AggEpidemioMalariaR.u5_total_tdr_tested_malaria_cases'
        db.delete_column(u'snisi_malaria_aggepidemiomalariar', 'u5_total_tdr_tested_malaria_cases')

        # Deleting field 'AggEpidemioMalariaR.pw_total_ge_parasite_pf_malaria_cases'
        db.delete_column(u'snisi_malaria_aggepidemiomalariar', 'pw_total_ge_parasite_pf_malaria_cases')

        # Deleting field 'AggEpidemioMalariaR.o5_total_ge_parasite_pf_malaria_cases'
        db.delete_column(u'snisi_malaria_aggepidemiomalariar', 'o5_total_ge_parasite_pf_malaria_cases')

        # Deleting field 'AggEpidemioMalariaR.o5_total_tdr_confirmed_malaria_cases'
        db.delete_column(u'snisi_malaria_aggepidemiomalariar', 'o5_total_tdr_confirmed_malaria_cases')

        # Deleting field 'AggEpidemioMalariaR.u5_total_tdr_parasite_pf_malaria_cases'
        db.delete_column(u'snisi_malaria_aggepidemiomalariar', 'u5_total_tdr_parasite_pf_malaria_cases')

        # Deleting field 'AggEpidemioMalariaR.u5_total_ge_parasite_pf_malaria_cases'
        db.delete_column(u'snisi_malaria_aggepidemiomalariar', 'u5_total_ge_parasite_pf_malaria_cases')

        # Deleting field 'AggEpidemioMalariaR.pw_total_tdr_confirmed_malaria_cases'
        db.delete_column(u'snisi_malaria_aggepidemiomalariar', 'pw_total_tdr_confirmed_malaria_cases')

        # Deleting field 'AggEpidemioMalariaR.u5_total_tdr_confirmed_malaria_cases'
        db.delete_column(u'snisi_malaria_aggepidemiomalariar', 'u5_total_tdr_confirmed_malaria_cases')

        # Deleting field 'AggEpidemioMalariaR.pw_total_tdr_parasite_pf_malaria_cases'
        db.delete_column(u'snisi_malaria_aggepidemiomalariar', 'pw_total_tdr_parasite_pf_malaria_cases')

        # Deleting field 'AggEpidemioMalariaR.o5_total_tdr_parasite_pf_malaria_cases'
        db.delete_column(u'snisi_malaria_aggepidemiomalariar', 'o5_total_tdr_parasite_pf_malaria_cases')

        # Deleting field 'AggEpidemioMalariaR.o5_total_ge_confirmed_malaria_cases'
        db.delete_column(u'snisi_malaria_aggepidemiomalariar', 'o5_total_ge_confirmed_malaria_cases')

        # Deleting field 'AggEpidemioMalariaR.pw_total_tdr_tested_malaria_cases'
        db.delete_column(u'snisi_malaria_aggepidemiomalariar', 'pw_total_tdr_tested_malaria_cases')

        # Adding field 'AggEpidemioMalariaR.u5_total_rdt_tested_malaria_cases'
        db.add_column(u'snisi_malaria_aggepidemiomalariar', 'u5_total_rdt_tested_malaria_cases',
                      self.gf('django.db.models.fields.PositiveIntegerField')(default=0),
                      keep_default=False)

        # Adding field 'AggEpidemioMalariaR.u5_total_rdt_confirmed_malaria_cases'
        db.add_column(u'snisi_malaria_aggepidemiomalariar', 'u5_total_rdt_confirmed_malaria_cases',
                      self.gf('django.db.models.fields.PositiveIntegerField')(default=0),
                      keep_default=False)

        # Adding field 'AggEpidemioMalariaR.u5_total_rdt_pfalciparum_malaria_cases'
        db.add_column(u'snisi_malaria_aggepidemiomalariar', 'u5_total_rdt_pfalciparum_malaria_cases',
                      self.gf('django.db.models.fields.PositiveIntegerField')(default=0),
                      keep_default=False)

        # Adding field 'AggEpidemioMalariaR.u5_total_ts_tested_malaria_cases'
        db.add_column(u'snisi_malaria_aggepidemiomalariar', 'u5_total_ts_tested_malaria_cases',
                      self.gf('django.db.models.fields.PositiveIntegerField')(default=0),
                      keep_default=False)

        # Adding field 'AggEpidemioMalariaR.u5_total_ts_confirmed_malaria_cases'
        db.add_column(u'snisi_malaria_aggepidemiomalariar', 'u5_total_ts_confirmed_malaria_cases',
                      self.gf('django.db.models.fields.PositiveIntegerField')(default=0),
                      keep_default=False)

        # Adding field 'AggEpidemioMalariaR.u5_total_ts_pfalciparum_malaria_cases'
        db.add_column(u'snisi_malaria_aggepidemiomalariar', 'u5_total_ts_pfalciparum_malaria_cases',
                      self.gf('django.db.models.fields.PositiveIntegerField')(default=0),
                      keep_default=False)

        # Adding field 'AggEpidemioMalariaR.o5_total_rdt_tested_malaria_cases'
        db.add_column(u'snisi_malaria_aggepidemiomalariar', 'o5_total_rdt_tested_malaria_cases',
                      self.gf('django.db.models.fields.PositiveIntegerField')(default=0),
                      keep_default=False)

        # Adding field 'AggEpidemioMalariaR.o5_total_rdt_confirmed_malaria_cases'
        db.add_column(u'snisi_malaria_aggepidemiomalariar', 'o5_total_rdt_confirmed_malaria_cases',
                      self.gf('django.db.models.fields.PositiveIntegerField')(default=0),
                      keep_default=False)

        # Adding field 'AggEpidemioMalariaR.o5_total_rdt_pfalciparum_malaria_cases'
        db.add_column(u'snisi_malaria_aggepidemiomalariar', 'o5_total_rdt_pfalciparum_malaria_cases',
                      self.gf('django.db.models.fields.PositiveIntegerField')(default=0),
                      keep_default=False)

        # Adding field 'AggEpidemioMalariaR.o5_total_ts_tested_malaria_cases'
        db.add_column(u'snisi_malaria_aggepidemiomalariar', 'o5_total_ts_tested_malaria_cases',
                      self.gf('django.db.models.fields.PositiveIntegerField')(default=0),
                      keep_default=False)

        # Adding field 'AggEpidemioMalariaR.o5_total_ts_confirmed_malaria_cases'
        db.add_column(u'snisi_malaria_aggepidemiomalariar', 'o5_total_ts_confirmed_malaria_cases',
                      self.gf('django.db.models.fields.PositiveIntegerField')(default=0),
                      keep_default=False)

        # Adding field 'AggEpidemioMalariaR.o5_total_ts_pfalciparum_malaria_cases'
        db.add_column(u'snisi_malaria_aggepidemiomalariar', 'o5_total_ts_pfalciparum_malaria_cases',
                      self.gf('django.db.models.fields.PositiveIntegerField')(default=0),
                      keep_default=False)

        # Adding field 'AggEpidemioMalariaR.pw_total_rdt_tested_malaria_cases'
        db.add_column(u'snisi_malaria_aggepidemiomalariar', 'pw_total_rdt_tested_malaria_cases',
                      self.gf('django.db.models.fields.PositiveIntegerField')(default=0),
                      keep_default=False)

        # Adding field 'AggEpidemioMalariaR.pw_total_rdt_confirmed_malaria_cases'
        db.add_column(u'snisi_malaria_aggepidemiomalariar', 'pw_total_rdt_confirmed_malaria_cases',
                      self.gf('django.db.models.fields.PositiveIntegerField')(default=0),
                      keep_default=False)

        # Adding field 'AggEpidemioMalariaR.pw_total_rdt_pfalciparum_malaria_cases'
        db.add_column(u'snisi_malaria_aggepidemiomalariar', 'pw_total_rdt_pfalciparum_malaria_cases',
                      self.gf('django.db.models.fields.PositiveIntegerField')(default=0),
                      keep_default=False)

        # Adding field 'AggEpidemioMalariaR.pw_total_ts_tested_malaria_cases'
        db.add_column(u'snisi_malaria_aggepidemiomalariar', 'pw_total_ts_tested_malaria_cases',
                      self.gf('django.db.models.fields.PositiveIntegerField')(default=0),
                      keep_default=False)

        # Adding field 'AggEpidemioMalariaR.pw_total_ts_confirmed_malaria_cases'
        db.add_column(u'snisi_malaria_aggepidemiomalariar', 'pw_total_ts_confirmed_malaria_cases',
                      self.gf('django.db.models.fields.PositiveIntegerField')(default=0),
                      keep_default=False)

        # Adding field 'AggEpidemioMalariaR.pw_total_ts_pfalciparum_malaria_cases'
        db.add_column(u'snisi_malaria_aggepidemiomalariar', 'pw_total_ts_pfalciparum_malaria_cases',
                      self.gf('django.db.models.fields.PositiveIntegerField')(default=0),
                      keep_default=False)


    def backwards(self, orm):

        # User chose to not deal with backwards NULL issues for 'EpidemioMalariaR.u5_total_ge_parasite_pf_malaria_cases'
        raise RuntimeError("Cannot reverse this migration. 'EpidemioMalariaR.u5_total_ge_parasite_pf_malaria_cases' and its values cannot be restored.")
        
        # The following code is provided here to aid in writing a correct migration        # Adding field 'EpidemioMalariaR.u5_total_ge_parasite_pf_malaria_cases'
        db.add_column(u'snisi_malaria_epidemiomalariar', 'u5_total_ge_parasite_pf_malaria_cases',
                      self.gf('django.db.models.fields.PositiveIntegerField')(),
                      keep_default=False)


        # User chose to not deal with backwards NULL issues for 'EpidemioMalariaR.u5_total_tdr_parasite_pf_malaria_cases'
        raise RuntimeError("Cannot reverse this migration. 'EpidemioMalariaR.u5_total_tdr_parasite_pf_malaria_cases' and its values cannot be restored.")
        
        # The following code is provided here to aid in writing a correct migration        # Adding field 'EpidemioMalariaR.u5_total_tdr_parasite_pf_malaria_cases'
        db.add_column(u'snisi_malaria_epidemiomalariar', 'u5_total_tdr_parasite_pf_malaria_cases',
                      self.gf('django.db.models.fields.PositiveIntegerField')(),
                      keep_default=False)


        # User chose to not deal with backwards NULL issues for 'EpidemioMalariaR.o5_total_tdr_confirmed_malaria_cases'
        raise RuntimeError("Cannot reverse this migration. 'EpidemioMalariaR.o5_total_tdr_confirmed_malaria_cases' and its values cannot be restored.")
        
        # The following code is provided here to aid in writing a correct migration        # Adding field 'EpidemioMalariaR.o5_total_tdr_confirmed_malaria_cases'
        db.add_column(u'snisi_malaria_epidemiomalariar', 'o5_total_tdr_confirmed_malaria_cases',
                      self.gf('django.db.models.fields.PositiveIntegerField')(),
                      keep_default=False)


        # User chose to not deal with backwards NULL issues for 'EpidemioMalariaR.o5_total_ge_tested_malaria_cases'
        raise RuntimeError("Cannot reverse this migration. 'EpidemioMalariaR.o5_total_ge_tested_malaria_cases' and its values cannot be restored.")
        
        # The following code is provided here to aid in writing a correct migration        # Adding field 'EpidemioMalariaR.o5_total_ge_tested_malaria_cases'
        db.add_column(u'snisi_malaria_epidemiomalariar', 'o5_total_ge_tested_malaria_cases',
                      self.gf('django.db.models.fields.PositiveIntegerField')(),
                      keep_default=False)


        # User chose to not deal with backwards NULL issues for 'EpidemioMalariaR.u5_total_ge_confirmed_malaria_cases'
        raise RuntimeError("Cannot reverse this migration. 'EpidemioMalariaR.u5_total_ge_confirmed_malaria_cases' and its values cannot be restored.")
        
        # The following code is provided here to aid in writing a correct migration        # Adding field 'EpidemioMalariaR.u5_total_ge_confirmed_malaria_cases'
        db.add_column(u'snisi_malaria_epidemiomalariar', 'u5_total_ge_confirmed_malaria_cases',
                      self.gf('django.db.models.fields.PositiveIntegerField')(),
                      keep_default=False)


        # User chose to not deal with backwards NULL issues for 'EpidemioMalariaR.u5_total_tdr_confirmed_malaria_cases'
        raise RuntimeError("Cannot reverse this migration. 'EpidemioMalariaR.u5_total_tdr_confirmed_malaria_cases' and its values cannot be restored.")
        
        # The following code is provided here to aid in writing a correct migration        # Adding field 'EpidemioMalariaR.u5_total_tdr_confirmed_malaria_cases'
        db.add_column(u'snisi_malaria_epidemiomalariar', 'u5_total_tdr_confirmed_malaria_cases',
                      self.gf('django.db.models.fields.PositiveIntegerField')(),
                      keep_default=False)


        # User chose to not deal with backwards NULL issues for 'EpidemioMalariaR.pw_total_ge_tested_malaria_cases'
        raise RuntimeError("Cannot reverse this migration. 'EpidemioMalariaR.pw_total_ge_tested_malaria_cases' and its values cannot be restored.")
        
        # The following code is provided here to aid in writing a correct migration        # Adding field 'EpidemioMalariaR.pw_total_ge_tested_malaria_cases'
        db.add_column(u'snisi_malaria_epidemiomalariar', 'pw_total_ge_tested_malaria_cases',
                      self.gf('django.db.models.fields.PositiveIntegerField')(),
                      keep_default=False)


        # User chose to not deal with backwards NULL issues for 'EpidemioMalariaR.u5_total_tdr_tested_malaria_cases'
        raise RuntimeError("Cannot reverse this migration. 'EpidemioMalariaR.u5_total_tdr_tested_malaria_cases' and its values cannot be restored.")
        
        # The following code is provided here to aid in writing a correct migration        # Adding field 'EpidemioMalariaR.u5_total_tdr_tested_malaria_cases'
        db.add_column(u'snisi_malaria_epidemiomalariar', 'u5_total_tdr_tested_malaria_cases',
                      self.gf('django.db.models.fields.PositiveIntegerField')(),
                      keep_default=False)


        # User chose to not deal with backwards NULL issues for 'EpidemioMalariaR.u5_total_ge_tested_malaria_cases'
        raise RuntimeError("Cannot reverse this migration. 'EpidemioMalariaR.u5_total_ge_tested_malaria_cases' and its values cannot be restored.")
        
        # The following code is provided here to aid in writing a correct migration        # Adding field 'EpidemioMalariaR.u5_total_ge_tested_malaria_cases'
        db.add_column(u'snisi_malaria_epidemiomalariar', 'u5_total_ge_tested_malaria_cases',
                      self.gf('django.db.models.fields.PositiveIntegerField')(),
                      keep_default=False)


        # User chose to not deal with backwards NULL issues for 'EpidemioMalariaR.pw_total_tdr_parasite_pf_malaria_cases'
        raise RuntimeError("Cannot reverse this migration. 'EpidemioMalariaR.pw_total_tdr_parasite_pf_malaria_cases' and its values cannot be restored.")
        
        # The following code is provided here to aid in writing a correct migration        # Adding field 'EpidemioMalariaR.pw_total_tdr_parasite_pf_malaria_cases'
        db.add_column(u'snisi_malaria_epidemiomalariar', 'pw_total_tdr_parasite_pf_malaria_cases',
                      self.gf('django.db.models.fields.PositiveIntegerField')(),
                      keep_default=False)


        # User chose to not deal with backwards NULL issues for 'EpidemioMalariaR.o5_total_tdr_tested_malaria_cases'
        raise RuntimeError("Cannot reverse this migration. 'EpidemioMalariaR.o5_total_tdr_tested_malaria_cases' and its values cannot be restored.")
        
        # The following code is provided here to aid in writing a correct migration        # Adding field 'EpidemioMalariaR.o5_total_tdr_tested_malaria_cases'
        db.add_column(u'snisi_malaria_epidemiomalariar', 'o5_total_tdr_tested_malaria_cases',
                      self.gf('django.db.models.fields.PositiveIntegerField')(),
                      keep_default=False)


        # User chose to not deal with backwards NULL issues for 'EpidemioMalariaR.pw_total_ge_confirmed_malaria_cases'
        raise RuntimeError("Cannot reverse this migration. 'EpidemioMalariaR.pw_total_ge_confirmed_malaria_cases' and its values cannot be restored.")
        
        # The following code is provided here to aid in writing a correct migration        # Adding field 'EpidemioMalariaR.pw_total_ge_confirmed_malaria_cases'
        db.add_column(u'snisi_malaria_epidemiomalariar', 'pw_total_ge_confirmed_malaria_cases',
                      self.gf('django.db.models.fields.PositiveIntegerField')(),
                      keep_default=False)


        # User chose to not deal with backwards NULL issues for 'EpidemioMalariaR.o5_total_tdr_parasite_pf_malaria_cases'
        raise RuntimeError("Cannot reverse this migration. 'EpidemioMalariaR.o5_total_tdr_parasite_pf_malaria_cases' and its values cannot be restored.")
        
        # The following code is provided here to aid in writing a correct migration        # Adding field 'EpidemioMalariaR.o5_total_tdr_parasite_pf_malaria_cases'
        db.add_column(u'snisi_malaria_epidemiomalariar', 'o5_total_tdr_parasite_pf_malaria_cases',
                      self.gf('django.db.models.fields.PositiveIntegerField')(),
                      keep_default=False)


        # User chose to not deal with backwards NULL issues for 'EpidemioMalariaR.o5_total_ge_confirmed_malaria_cases'
        raise RuntimeError("Cannot reverse this migration. 'EpidemioMalariaR.o5_total_ge_confirmed_malaria_cases' and its values cannot be restored.")
        
        # The following code is provided here to aid in writing a correct migration        # Adding field 'EpidemioMalariaR.o5_total_ge_confirmed_malaria_cases'
        db.add_column(u'snisi_malaria_epidemiomalariar', 'o5_total_ge_confirmed_malaria_cases',
                      self.gf('django.db.models.fields.PositiveIntegerField')(),
                      keep_default=False)


        # User chose to not deal with backwards NULL issues for 'EpidemioMalariaR.pw_total_ge_parasite_pf_malaria_cases'
        raise RuntimeError("Cannot reverse this migration. 'EpidemioMalariaR.pw_total_ge_parasite_pf_malaria_cases' and its values cannot be restored.")
        
        # The following code is provided here to aid in writing a correct migration        # Adding field 'EpidemioMalariaR.pw_total_ge_parasite_pf_malaria_cases'
        db.add_column(u'snisi_malaria_epidemiomalariar', 'pw_total_ge_parasite_pf_malaria_cases',
                      self.gf('django.db.models.fields.PositiveIntegerField')(),
                      keep_default=False)


        # User chose to not deal with backwards NULL issues for 'EpidemioMalariaR.pw_total_tdr_confirmed_malaria_cases'
        raise RuntimeError("Cannot reverse this migration. 'EpidemioMalariaR.pw_total_tdr_confirmed_malaria_cases' and its values cannot be restored.")
        
        # The following code is provided here to aid in writing a correct migration        # Adding field 'EpidemioMalariaR.pw_total_tdr_confirmed_malaria_cases'
        db.add_column(u'snisi_malaria_epidemiomalariar', 'pw_total_tdr_confirmed_malaria_cases',
                      self.gf('django.db.models.fields.PositiveIntegerField')(),
                      keep_default=False)


        # User chose to not deal with backwards NULL issues for 'EpidemioMalariaR.pw_total_tdr_tested_malaria_cases'
        raise RuntimeError("Cannot reverse this migration. 'EpidemioMalariaR.pw_total_tdr_tested_malaria_cases' and its values cannot be restored.")
        
        # The following code is provided here to aid in writing a correct migration        # Adding field 'EpidemioMalariaR.pw_total_tdr_tested_malaria_cases'
        db.add_column(u'snisi_malaria_epidemiomalariar', 'pw_total_tdr_tested_malaria_cases',
                      self.gf('django.db.models.fields.PositiveIntegerField')(),
                      keep_default=False)


        # User chose to not deal with backwards NULL issues for 'EpidemioMalariaR.o5_total_ge_parasite_pf_malaria_cases'
        raise RuntimeError("Cannot reverse this migration. 'EpidemioMalariaR.o5_total_ge_parasite_pf_malaria_cases' and its values cannot be restored.")
        
        # The following code is provided here to aid in writing a correct migration        # Adding field 'EpidemioMalariaR.o5_total_ge_parasite_pf_malaria_cases'
        db.add_column(u'snisi_malaria_epidemiomalariar', 'o5_total_ge_parasite_pf_malaria_cases',
                      self.gf('django.db.models.fields.PositiveIntegerField')(),
                      keep_default=False)

        # Deleting field 'EpidemioMalariaR.u5_total_rdt_tested_malaria_cases'
        db.delete_column(u'snisi_malaria_epidemiomalariar', 'u5_total_rdt_tested_malaria_cases')

        # Deleting field 'EpidemioMalariaR.u5_total_rdt_confirmed_malaria_cases'
        db.delete_column(u'snisi_malaria_epidemiomalariar', 'u5_total_rdt_confirmed_malaria_cases')

        # Deleting field 'EpidemioMalariaR.u5_total_rdt_pfalciparum_malaria_cases'
        db.delete_column(u'snisi_malaria_epidemiomalariar', 'u5_total_rdt_pfalciparum_malaria_cases')

        # Deleting field 'EpidemioMalariaR.u5_total_ts_tested_malaria_cases'
        db.delete_column(u'snisi_malaria_epidemiomalariar', 'u5_total_ts_tested_malaria_cases')

        # Deleting field 'EpidemioMalariaR.u5_total_ts_confirmed_malaria_cases'
        db.delete_column(u'snisi_malaria_epidemiomalariar', 'u5_total_ts_confirmed_malaria_cases')

        # Deleting field 'EpidemioMalariaR.u5_total_ts_pfalciparum_malaria_cases'
        db.delete_column(u'snisi_malaria_epidemiomalariar', 'u5_total_ts_pfalciparum_malaria_cases')

        # Deleting field 'EpidemioMalariaR.o5_total_rdt_tested_malaria_cases'
        db.delete_column(u'snisi_malaria_epidemiomalariar', 'o5_total_rdt_tested_malaria_cases')

        # Deleting field 'EpidemioMalariaR.o5_total_rdt_confirmed_malaria_cases'
        db.delete_column(u'snisi_malaria_epidemiomalariar', 'o5_total_rdt_confirmed_malaria_cases')

        # Deleting field 'EpidemioMalariaR.o5_total_rdt_pfalciparum_malaria_cases'
        db.delete_column(u'snisi_malaria_epidemiomalariar', 'o5_total_rdt_pfalciparum_malaria_cases')

        # Deleting field 'EpidemioMalariaR.o5_total_ts_tested_malaria_cases'
        db.delete_column(u'snisi_malaria_epidemiomalariar', 'o5_total_ts_tested_malaria_cases')

        # Deleting field 'EpidemioMalariaR.o5_total_ts_confirmed_malaria_cases'
        db.delete_column(u'snisi_malaria_epidemiomalariar', 'o5_total_ts_confirmed_malaria_cases')

        # Deleting field 'EpidemioMalariaR.o5_total_ts_pfalciparum_malaria_cases'
        db.delete_column(u'snisi_malaria_epidemiomalariar', 'o5_total_ts_pfalciparum_malaria_cases')

        # Deleting field 'EpidemioMalariaR.pw_total_rdt_tested_malaria_cases'
        db.delete_column(u'snisi_malaria_epidemiomalariar', 'pw_total_rdt_tested_malaria_cases')

        # Deleting field 'EpidemioMalariaR.pw_total_rdt_confirmed_malaria_cases'
        db.delete_column(u'snisi_malaria_epidemiomalariar', 'pw_total_rdt_confirmed_malaria_cases')

        # Deleting field 'EpidemioMalariaR.pw_total_rdt_pfalciparum_malaria_cases'
        db.delete_column(u'snisi_malaria_epidemiomalariar', 'pw_total_rdt_pfalciparum_malaria_cases')

        # Deleting field 'EpidemioMalariaR.pw_total_ts_tested_malaria_cases'
        db.delete_column(u'snisi_malaria_epidemiomalariar', 'pw_total_ts_tested_malaria_cases')

        # Deleting field 'EpidemioMalariaR.pw_total_ts_confirmed_malaria_cases'
        db.delete_column(u'snisi_malaria_epidemiomalariar', 'pw_total_ts_confirmed_malaria_cases')

        # Deleting field 'EpidemioMalariaR.pw_total_ts_pfalciparum_malaria_cases'
        db.delete_column(u'snisi_malaria_epidemiomalariar', 'pw_total_ts_pfalciparum_malaria_cases')


        # User chose to not deal with backwards NULL issues for 'AggEpidemioMalariaR.pw_total_ge_tested_malaria_cases'
        raise RuntimeError("Cannot reverse this migration. 'AggEpidemioMalariaR.pw_total_ge_tested_malaria_cases' and its values cannot be restored.")
        
        # The following code is provided here to aid in writing a correct migration        # Adding field 'AggEpidemioMalariaR.pw_total_ge_tested_malaria_cases'
        db.add_column(u'snisi_malaria_aggepidemiomalariar', 'pw_total_ge_tested_malaria_cases',
                      self.gf('django.db.models.fields.PositiveIntegerField')(),
                      keep_default=False)


        # User chose to not deal with backwards NULL issues for 'AggEpidemioMalariaR.pw_total_ge_confirmed_malaria_cases'
        raise RuntimeError("Cannot reverse this migration. 'AggEpidemioMalariaR.pw_total_ge_confirmed_malaria_cases' and its values cannot be restored.")
        
        # The following code is provided here to aid in writing a correct migration        # Adding field 'AggEpidemioMalariaR.pw_total_ge_confirmed_malaria_cases'
        db.add_column(u'snisi_malaria_aggepidemiomalariar', 'pw_total_ge_confirmed_malaria_cases',
                      self.gf('django.db.models.fields.PositiveIntegerField')(),
                      keep_default=False)


        # User chose to not deal with backwards NULL issues for 'AggEpidemioMalariaR.o5_total_tdr_tested_malaria_cases'
        raise RuntimeError("Cannot reverse this migration. 'AggEpidemioMalariaR.o5_total_tdr_tested_malaria_cases' and its values cannot be restored.")
        
        # The following code is provided here to aid in writing a correct migration        # Adding field 'AggEpidemioMalariaR.o5_total_tdr_tested_malaria_cases'
        db.add_column(u'snisi_malaria_aggepidemiomalariar', 'o5_total_tdr_tested_malaria_cases',
                      self.gf('django.db.models.fields.PositiveIntegerField')(),
                      keep_default=False)


        # User chose to not deal with backwards NULL issues for 'AggEpidemioMalariaR.u5_total_ge_tested_malaria_cases'
        raise RuntimeError("Cannot reverse this migration. 'AggEpidemioMalariaR.u5_total_ge_tested_malaria_cases' and its values cannot be restored.")
        
        # The following code is provided here to aid in writing a correct migration        # Adding field 'AggEpidemioMalariaR.u5_total_ge_tested_malaria_cases'
        db.add_column(u'snisi_malaria_aggepidemiomalariar', 'u5_total_ge_tested_malaria_cases',
                      self.gf('django.db.models.fields.PositiveIntegerField')(),
                      keep_default=False)


        # User chose to not deal with backwards NULL issues for 'AggEpidemioMalariaR.u5_total_ge_confirmed_malaria_cases'
        raise RuntimeError("Cannot reverse this migration. 'AggEpidemioMalariaR.u5_total_ge_confirmed_malaria_cases' and its values cannot be restored.")
        
        # The following code is provided here to aid in writing a correct migration        # Adding field 'AggEpidemioMalariaR.u5_total_ge_confirmed_malaria_cases'
        db.add_column(u'snisi_malaria_aggepidemiomalariar', 'u5_total_ge_confirmed_malaria_cases',
                      self.gf('django.db.models.fields.PositiveIntegerField')(),
                      keep_default=False)


        # User chose to not deal with backwards NULL issues for 'AggEpidemioMalariaR.o5_total_ge_tested_malaria_cases'
        raise RuntimeError("Cannot reverse this migration. 'AggEpidemioMalariaR.o5_total_ge_tested_malaria_cases' and its values cannot be restored.")
        
        # The following code is provided here to aid in writing a correct migration        # Adding field 'AggEpidemioMalariaR.o5_total_ge_tested_malaria_cases'
        db.add_column(u'snisi_malaria_aggepidemiomalariar', 'o5_total_ge_tested_malaria_cases',
                      self.gf('django.db.models.fields.PositiveIntegerField')(),
                      keep_default=False)


        # User chose to not deal with backwards NULL issues for 'AggEpidemioMalariaR.u5_total_tdr_tested_malaria_cases'
        raise RuntimeError("Cannot reverse this migration. 'AggEpidemioMalariaR.u5_total_tdr_tested_malaria_cases' and its values cannot be restored.")
        
        # The following code is provided here to aid in writing a correct migration        # Adding field 'AggEpidemioMalariaR.u5_total_tdr_tested_malaria_cases'
        db.add_column(u'snisi_malaria_aggepidemiomalariar', 'u5_total_tdr_tested_malaria_cases',
                      self.gf('django.db.models.fields.PositiveIntegerField')(),
                      keep_default=False)


        # User chose to not deal with backwards NULL issues for 'AggEpidemioMalariaR.pw_total_ge_parasite_pf_malaria_cases'
        raise RuntimeError("Cannot reverse this migration. 'AggEpidemioMalariaR.pw_total_ge_parasite_pf_malaria_cases' and its values cannot be restored.")
        
        # The following code is provided here to aid in writing a correct migration        # Adding field 'AggEpidemioMalariaR.pw_total_ge_parasite_pf_malaria_cases'
        db.add_column(u'snisi_malaria_aggepidemiomalariar', 'pw_total_ge_parasite_pf_malaria_cases',
                      self.gf('django.db.models.fields.PositiveIntegerField')(),
                      keep_default=False)


        # User chose to not deal with backwards NULL issues for 'AggEpidemioMalariaR.o5_total_ge_parasite_pf_malaria_cases'
        raise RuntimeError("Cannot reverse this migration. 'AggEpidemioMalariaR.o5_total_ge_parasite_pf_malaria_cases' and its values cannot be restored.")
        
        # The following code is provided here to aid in writing a correct migration        # Adding field 'AggEpidemioMalariaR.o5_total_ge_parasite_pf_malaria_cases'
        db.add_column(u'snisi_malaria_aggepidemiomalariar', 'o5_total_ge_parasite_pf_malaria_cases',
                      self.gf('django.db.models.fields.PositiveIntegerField')(),
                      keep_default=False)


        # User chose to not deal with backwards NULL issues for 'AggEpidemioMalariaR.o5_total_tdr_confirmed_malaria_cases'
        raise RuntimeError("Cannot reverse this migration. 'AggEpidemioMalariaR.o5_total_tdr_confirmed_malaria_cases' and its values cannot be restored.")
        
        # The following code is provided here to aid in writing a correct migration        # Adding field 'AggEpidemioMalariaR.o5_total_tdr_confirmed_malaria_cases'
        db.add_column(u'snisi_malaria_aggepidemiomalariar', 'o5_total_tdr_confirmed_malaria_cases',
                      self.gf('django.db.models.fields.PositiveIntegerField')(),
                      keep_default=False)


        # User chose to not deal with backwards NULL issues for 'AggEpidemioMalariaR.u5_total_tdr_parasite_pf_malaria_cases'
        raise RuntimeError("Cannot reverse this migration. 'AggEpidemioMalariaR.u5_total_tdr_parasite_pf_malaria_cases' and its values cannot be restored.")
        
        # The following code is provided here to aid in writing a correct migration        # Adding field 'AggEpidemioMalariaR.u5_total_tdr_parasite_pf_malaria_cases'
        db.add_column(u'snisi_malaria_aggepidemiomalariar', 'u5_total_tdr_parasite_pf_malaria_cases',
                      self.gf('django.db.models.fields.PositiveIntegerField')(),
                      keep_default=False)


        # User chose to not deal with backwards NULL issues for 'AggEpidemioMalariaR.u5_total_ge_parasite_pf_malaria_cases'
        raise RuntimeError("Cannot reverse this migration. 'AggEpidemioMalariaR.u5_total_ge_parasite_pf_malaria_cases' and its values cannot be restored.")
        
        # The following code is provided here to aid in writing a correct migration        # Adding field 'AggEpidemioMalariaR.u5_total_ge_parasite_pf_malaria_cases'
        db.add_column(u'snisi_malaria_aggepidemiomalariar', 'u5_total_ge_parasite_pf_malaria_cases',
                      self.gf('django.db.models.fields.PositiveIntegerField')(),
                      keep_default=False)


        # User chose to not deal with backwards NULL issues for 'AggEpidemioMalariaR.pw_total_tdr_confirmed_malaria_cases'
        raise RuntimeError("Cannot reverse this migration. 'AggEpidemioMalariaR.pw_total_tdr_confirmed_malaria_cases' and its values cannot be restored.")
        
        # The following code is provided here to aid in writing a correct migration        # Adding field 'AggEpidemioMalariaR.pw_total_tdr_confirmed_malaria_cases'
        db.add_column(u'snisi_malaria_aggepidemiomalariar', 'pw_total_tdr_confirmed_malaria_cases',
                      self.gf('django.db.models.fields.PositiveIntegerField')(),
                      keep_default=False)


        # User chose to not deal with backwards NULL issues for 'AggEpidemioMalariaR.u5_total_tdr_confirmed_malaria_cases'
        raise RuntimeError("Cannot reverse this migration. 'AggEpidemioMalariaR.u5_total_tdr_confirmed_malaria_cases' and its values cannot be restored.")
        
        # The following code is provided here to aid in writing a correct migration        # Adding field 'AggEpidemioMalariaR.u5_total_tdr_confirmed_malaria_cases'
        db.add_column(u'snisi_malaria_aggepidemiomalariar', 'u5_total_tdr_confirmed_malaria_cases',
                      self.gf('django.db.models.fields.PositiveIntegerField')(),
                      keep_default=False)


        # User chose to not deal with backwards NULL issues for 'AggEpidemioMalariaR.pw_total_tdr_parasite_pf_malaria_cases'
        raise RuntimeError("Cannot reverse this migration. 'AggEpidemioMalariaR.pw_total_tdr_parasite_pf_malaria_cases' and its values cannot be restored.")
        
        # The following code is provided here to aid in writing a correct migration        # Adding field 'AggEpidemioMalariaR.pw_total_tdr_parasite_pf_malaria_cases'
        db.add_column(u'snisi_malaria_aggepidemiomalariar', 'pw_total_tdr_parasite_pf_malaria_cases',
                      self.gf('django.db.models.fields.PositiveIntegerField')(),
                      keep_default=False)


        # User chose to not deal with backwards NULL issues for 'AggEpidemioMalariaR.o5_total_tdr_parasite_pf_malaria_cases'
        raise RuntimeError("Cannot reverse this migration. 'AggEpidemioMalariaR.o5_total_tdr_parasite_pf_malaria_cases' and its values cannot be restored.")
        
        # The following code is provided here to aid in writing a correct migration        # Adding field 'AggEpidemioMalariaR.o5_total_tdr_parasite_pf_malaria_cases'
        db.add_column(u'snisi_malaria_aggepidemiomalariar', 'o5_total_tdr_parasite_pf_malaria_cases',
                      self.gf('django.db.models.fields.PositiveIntegerField')(),
                      keep_default=False)


        # User chose to not deal with backwards NULL issues for 'AggEpidemioMalariaR.o5_total_ge_confirmed_malaria_cases'
        raise RuntimeError("Cannot reverse this migration. 'AggEpidemioMalariaR.o5_total_ge_confirmed_malaria_cases' and its values cannot be restored.")
        
        # The following code is provided here to aid in writing a correct migration        # Adding field 'AggEpidemioMalariaR.o5_total_ge_confirmed_malaria_cases'
        db.add_column(u'snisi_malaria_aggepidemiomalariar', 'o5_total_ge_confirmed_malaria_cases',
                      self.gf('django.db.models.fields.PositiveIntegerField')(),
                      keep_default=False)


        # User chose to not deal with backwards NULL issues for 'AggEpidemioMalariaR.pw_total_tdr_tested_malaria_cases'
        raise RuntimeError("Cannot reverse this migration. 'AggEpidemioMalariaR.pw_total_tdr_tested_malaria_cases' and its values cannot be restored.")
        
        # The following code is provided here to aid in writing a correct migration        # Adding field 'AggEpidemioMalariaR.pw_total_tdr_tested_malaria_cases'
        db.add_column(u'snisi_malaria_aggepidemiomalariar', 'pw_total_tdr_tested_malaria_cases',
                      self.gf('django.db.models.fields.PositiveIntegerField')(),
                      keep_default=False)

        # Deleting field 'AggEpidemioMalariaR.u5_total_rdt_tested_malaria_cases'
        db.delete_column(u'snisi_malaria_aggepidemiomalariar', 'u5_total_rdt_tested_malaria_cases')

        # Deleting field 'AggEpidemioMalariaR.u5_total_rdt_confirmed_malaria_cases'
        db.delete_column(u'snisi_malaria_aggepidemiomalariar', 'u5_total_rdt_confirmed_malaria_cases')

        # Deleting field 'AggEpidemioMalariaR.u5_total_rdt_pfalciparum_malaria_cases'
        db.delete_column(u'snisi_malaria_aggepidemiomalariar', 'u5_total_rdt_pfalciparum_malaria_cases')

        # Deleting field 'AggEpidemioMalariaR.u5_total_ts_tested_malaria_cases'
        db.delete_column(u'snisi_malaria_aggepidemiomalariar', 'u5_total_ts_tested_malaria_cases')

        # Deleting field 'AggEpidemioMalariaR.u5_total_ts_confirmed_malaria_cases'
        db.delete_column(u'snisi_malaria_aggepidemiomalariar', 'u5_total_ts_confirmed_malaria_cases')

        # Deleting field 'AggEpidemioMalariaR.u5_total_ts_pfalciparum_malaria_cases'
        db.delete_column(u'snisi_malaria_aggepidemiomalariar', 'u5_total_ts_pfalciparum_malaria_cases')

        # Deleting field 'AggEpidemioMalariaR.o5_total_rdt_tested_malaria_cases'
        db.delete_column(u'snisi_malaria_aggepidemiomalariar', 'o5_total_rdt_tested_malaria_cases')

        # Deleting field 'AggEpidemioMalariaR.o5_total_rdt_confirmed_malaria_cases'
        db.delete_column(u'snisi_malaria_aggepidemiomalariar', 'o5_total_rdt_confirmed_malaria_cases')

        # Deleting field 'AggEpidemioMalariaR.o5_total_rdt_pfalciparum_malaria_cases'
        db.delete_column(u'snisi_malaria_aggepidemiomalariar', 'o5_total_rdt_pfalciparum_malaria_cases')

        # Deleting field 'AggEpidemioMalariaR.o5_total_ts_tested_malaria_cases'
        db.delete_column(u'snisi_malaria_aggepidemiomalariar', 'o5_total_ts_tested_malaria_cases')

        # Deleting field 'AggEpidemioMalariaR.o5_total_ts_confirmed_malaria_cases'
        db.delete_column(u'snisi_malaria_aggepidemiomalariar', 'o5_total_ts_confirmed_malaria_cases')

        # Deleting field 'AggEpidemioMalariaR.o5_total_ts_pfalciparum_malaria_cases'
        db.delete_column(u'snisi_malaria_aggepidemiomalariar', 'o5_total_ts_pfalciparum_malaria_cases')

        # Deleting field 'AggEpidemioMalariaR.pw_total_rdt_tested_malaria_cases'
        db.delete_column(u'snisi_malaria_aggepidemiomalariar', 'pw_total_rdt_tested_malaria_cases')

        # Deleting field 'AggEpidemioMalariaR.pw_total_rdt_confirmed_malaria_cases'
        db.delete_column(u'snisi_malaria_aggepidemiomalariar', 'pw_total_rdt_confirmed_malaria_cases')

        # Deleting field 'AggEpidemioMalariaR.pw_total_rdt_pfalciparum_malaria_cases'
        db.delete_column(u'snisi_malaria_aggepidemiomalariar', 'pw_total_rdt_pfalciparum_malaria_cases')

        # Deleting field 'AggEpidemioMalariaR.pw_total_ts_tested_malaria_cases'
        db.delete_column(u'snisi_malaria_aggepidemiomalariar', 'pw_total_ts_tested_malaria_cases')

        # Deleting field 'AggEpidemioMalariaR.pw_total_ts_confirmed_malaria_cases'
        db.delete_column(u'snisi_malaria_aggepidemiomalariar', 'pw_total_ts_confirmed_malaria_cases')

        # Deleting field 'AggEpidemioMalariaR.pw_total_ts_pfalciparum_malaria_cases'
        db.delete_column(u'snisi_malaria_aggepidemiomalariar', 'pw_total_ts_pfalciparum_malaria_cases')


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
            'uuid': ('django.db.models.fields.CharField', [], {'default': "'c65a714a-5ef9-49d5-bb3b-5e2fa8bd2276'", 'max_length': '200', 'primary_key': 'True'}),
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
            'o5_total_consultation_all_causes': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'}),
            'o5_total_death_all_causes': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'}),
            'o5_total_malaria_death': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'}),
            'o5_total_rdt_confirmed_malaria_cases': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'}),
            'o5_total_rdt_pfalciparum_malaria_cases': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'}),
            'o5_total_rdt_tested_malaria_cases': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'}),
            'o5_total_severe_malaria_cases': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'}),
            'o5_total_simple_malaria_cases': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'}),
            'o5_total_suspected_malaria_cases': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'}),
            'o5_total_ts_confirmed_malaria_cases': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'}),
            'o5_total_ts_pfalciparum_malaria_cases': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'}),
            'o5_total_ts_tested_malaria_cases': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'}),
            'pw_total_consultation_all_causes': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'}),
            'pw_total_death_all_causes': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'}),
            'pw_total_malaria_death': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'}),
            'pw_total_rdt_confirmed_malaria_cases': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'}),
            'pw_total_rdt_pfalciparum_malaria_cases': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'}),
            'pw_total_rdt_tested_malaria_cases': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'}),
            'pw_total_severe_malaria_cases': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'}),
            'pw_total_simple_malaria_cases': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'}),
            'pw_total_suspected_malaria_cases': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'}),
            'pw_total_ts_confirmed_malaria_cases': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'}),
            'pw_total_ts_pfalciparum_malaria_cases': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'}),
            'pw_total_ts_tested_malaria_cases': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'}),
            u'snisireport_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['snisi_core.SNISIReport']", 'unique': 'True', 'primary_key': 'True'}),
            'u5_total_consultation_all_causes': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'}),
            'u5_total_death_all_causes': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'}),
            'u5_total_malaria_death': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'}),
            'u5_total_rdt_confirmed_malaria_cases': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'}),
            'u5_total_rdt_pfalciparum_malaria_cases': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'}),
            'u5_total_rdt_tested_malaria_cases': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'}),
            'u5_total_severe_malaria_cases': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'}),
            'u5_total_simple_malaria_cases': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'}),
            'u5_total_suspected_malaria_cases': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'}),
            'u5_total_ts_confirmed_malaria_cases': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'}),
            'u5_total_ts_pfalciparum_malaria_cases': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'}),
            'u5_total_ts_tested_malaria_cases': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'})
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
            'o5_total_consultation_all_causes': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'}),
            'o5_total_death_all_causes': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'}),
            'o5_total_malaria_death': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'}),
            'o5_total_rdt_confirmed_malaria_cases': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'}),
            'o5_total_rdt_pfalciparum_malaria_cases': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'}),
            'o5_total_rdt_tested_malaria_cases': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'}),
            'o5_total_severe_malaria_cases': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'}),
            'o5_total_simple_malaria_cases': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'}),
            'o5_total_suspected_malaria_cases': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'}),
            'o5_total_ts_confirmed_malaria_cases': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'}),
            'o5_total_ts_pfalciparum_malaria_cases': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'}),
            'o5_total_ts_tested_malaria_cases': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'}),
            'pw_total_consultation_all_causes': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'}),
            'pw_total_death_all_causes': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'}),
            'pw_total_malaria_death': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'}),
            'pw_total_rdt_confirmed_malaria_cases': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'}),
            'pw_total_rdt_pfalciparum_malaria_cases': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'}),
            'pw_total_rdt_tested_malaria_cases': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'}),
            'pw_total_severe_malaria_cases': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'}),
            'pw_total_simple_malaria_cases': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'}),
            'pw_total_suspected_malaria_cases': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'}),
            'pw_total_ts_confirmed_malaria_cases': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'}),
            'pw_total_ts_pfalciparum_malaria_cases': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'}),
            'pw_total_ts_tested_malaria_cases': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'}),
            u'snisireport_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['snisi_core.SNISIReport']", 'unique': 'True', 'primary_key': 'True'}),
            'u5_total_consultation_all_causes': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'}),
            'u5_total_death_all_causes': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'}),
            'u5_total_malaria_death': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'}),
            'u5_total_rdt_confirmed_malaria_cases': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'}),
            'u5_total_rdt_pfalciparum_malaria_cases': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'}),
            'u5_total_rdt_tested_malaria_cases': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'}),
            'u5_total_severe_malaria_cases': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'}),
            'u5_total_simple_malaria_cases': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'}),
            'u5_total_suspected_malaria_cases': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'}),
            'u5_total_ts_confirmed_malaria_cases': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'}),
            'u5_total_ts_pfalciparum_malaria_cases': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'}),
            'u5_total_ts_tested_malaria_cases': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'})
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