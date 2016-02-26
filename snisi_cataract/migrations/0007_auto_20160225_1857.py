# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('snisi_cataract', '0006_aggcatmissionr'),
    ]

    operations = [
        migrations.AddField(
            model_name='aggcatmissionr',
            name='direct_indiv_sources',
            field=models.ManyToManyField(related_name='direct_source_agg_aggcatmissionr_reports', verbose_name='Primary. Sources (direct)', to='snisi_cataract.CATMissionR', blank=True),
        ),
        migrations.AddField(
            model_name='aggcatmissionr',
            name='indiv_sources',
            field=models.ManyToManyField(related_name='source_agg_aggcatmissionr_reports', verbose_name='Primary. Sources', to='snisi_cataract.CATMissionR', blank=True),
        ),
    ]
