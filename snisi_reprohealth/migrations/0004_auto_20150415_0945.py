# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('snisi_reprohealth', '0003_auto_20141022_1400'),
    ]

    operations = [
        migrations.AlterField(
            model_name='aggpfactivitiesr',
            name='agg_sources',
            field=models.ManyToManyField(related_name='aggregated_agg_aggpfactivitiesr_reports', verbose_name='Aggr. Sources (all)', to='snisi_reprohealth.AggPFActivitiesR', blank=True),
        ),
        migrations.AlterField(
            model_name='aggpfactivitiesr',
            name='direct_agg_sources',
            field=models.ManyToManyField(related_name='direct_aggregated_agg_aggpfactivitiesr_reports', verbose_name='Aggr. Sources (direct)', to='snisi_reprohealth.AggPFActivitiesR', blank=True),
        ),
        migrations.AlterField(
            model_name='aggpfactivitiesr',
            name='direct_indiv_sources',
            field=models.ManyToManyField(related_name='direct_source_agg_aggpfactivitiesr_reports', verbose_name='Primary. Sources (direct)', to='snisi_reprohealth.PFActivitiesR', blank=True),
        ),
        migrations.AlterField(
            model_name='aggpfactivitiesr',
            name='indiv_sources',
            field=models.ManyToManyField(related_name='source_agg_aggpfactivitiesr_reports', verbose_name='Primary. Sources (all)', to='snisi_reprohealth.PFActivitiesR', blank=True),
        ),
    ]
