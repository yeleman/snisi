# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('snisi_core', '0010_auto_20150710_1405'),
        ('snisi_cataract', '0005_auto_20160225_1611'),
    ]

    operations = [
        migrations.CreateModel(
            name='AggCATMissionR',
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
                ('nb_surgery_male', models.PositiveIntegerField(default=0, verbose_name='Nb. surgeries Male')),
                ('nb_surgery_female', models.PositiveIntegerField(default=0, verbose_name='Nb. surgeries Female')),
                ('nb_surgery_right_eye', models.PositiveIntegerField(default=0, verbose_name='Nb. surgeries Right Eye')),
                ('nb_surgery_left_eye', models.PositiveIntegerField(default=0, verbose_name='Nb. surgeries Left Eye')),
                ('nb_age_under_15', models.PositiveIntegerField(default=0, verbose_name='Nb. surgeries Patient under 15')),
                ('nb_age_under_18', models.PositiveIntegerField(default=0, verbose_name='Nb. surgeries Patient under 18')),
                ('nb_age_under_20', models.PositiveIntegerField(default=0, verbose_name='Nb. surgeries Patient under 20')),
                ('nb_age_under_25', models.PositiveIntegerField(default=0, verbose_name='Nb. surgeries Patient under 25')),
                ('nb_age_under_30', models.PositiveIntegerField(default=0, verbose_name='Nb. surgeries Patient under 30')),
                ('nb_age_under_35', models.PositiveIntegerField(default=0, verbose_name='Nb. surgeries Patient under 35')),
                ('nb_age_under_40', models.PositiveIntegerField(default=0, verbose_name='Nb. surgeries Patient under 40')),
                ('nb_age_under_45', models.PositiveIntegerField(default=0, verbose_name='Nb. surgeries Patient under 45')),
                ('nb_age_under_50', models.PositiveIntegerField(default=0, verbose_name='Nb. surgeries Patient under 50')),
                ('nb_age_over_50', models.PositiveIntegerField(default=0, verbose_name='Nb. surgeries Patient over 50')),
                ('nb_surgery_reports', models.PositiveIntegerField(default=0, verbose_name='Nb of surgeries')),
                ('result_delay_min', models.PositiveIntegerField(default=0)),
                ('result_delay_max', models.PositiveIntegerField(default=0)),
                ('result_delay_mean', models.FloatField(default=0)),
                ('result_delay_median', models.FloatField(default=0)),
                ('result_delay_total', models.PositiveIntegerField(default=0)),
                ('visual_acuity_min', models.PositiveIntegerField(default=0)),
                ('visual_acuity_max', models.PositiveIntegerField(default=0)),
                ('visual_acuity_mean', models.FloatField(default=0)),
                ('visual_acuity_median', models.FloatField(default=0)),
                ('agg_sources', models.ManyToManyField(related_name='aggregated_agg_aggcatmissionr_reports', verbose_name='Aggr. Sources (all)', to='snisi_cataract.AggCATMissionR', blank=True)),
                ('direct_agg_sources', models.ManyToManyField(related_name='direct_aggregated_agg_aggcatmissionr_reports', verbose_name='Aggr. Sources (direct)', to='snisi_cataract.AggCATMissionR', blank=True)),
            ],
            options={
                'verbose_name': 'Aggregated CAT Surgery Mission Report',
                'verbose_name_plural': 'Aggregated CAT Surgery Mission Reports',
            },
            bases=('snisi_core.snisireport', models.Model),
        ),
    ]
