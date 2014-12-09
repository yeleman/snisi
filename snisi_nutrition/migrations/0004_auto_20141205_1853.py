# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('snisi_nutrition', '0003_auto_20141128_1833'),
    ]

    operations = [
        migrations.AddField(
            model_name='aggnutritionr',
            name='direct_indiv_sources',
            field=models.ManyToManyField(related_name='direct_source_agg_aggnutritionr_reports', null=True, verbose_name='Primary. Sources (direct)', to='snisi_nutrition.NutritionR', blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='aggnutritionstocksr',
            name='direct_indiv_sources',
            field=models.ManyToManyField(related_name='direct_source_agg_aggnutritionstocksr_reports', null=True, verbose_name='Primary. Sources (direct)', to='snisi_nutrition.NutritionStocksR', blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='aggurenamnutritionr',
            name='direct_indiv_sources',
            field=models.ManyToManyField(related_name='direct_source_agg_aggurenamnutritionr_reports', null=True, verbose_name='Primary. Sources (direct)', to='snisi_nutrition.URENAMNutritionR', blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='aggurenasnutritionr',
            name='direct_indiv_sources',
            field=models.ManyToManyField(related_name='direct_source_agg_aggurenasnutritionr_reports', null=True, verbose_name='Primary. Sources (direct)', to='snisi_nutrition.URENASNutritionR', blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='aggureninutritionr',
            name='direct_indiv_sources',
            field=models.ManyToManyField(related_name='direct_source_agg_aggureninutritionr_reports', null=True, verbose_name='Primary. Sources (direct)', to='snisi_nutrition.URENINutritionR', blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='aggweeklynutritionr',
            name='direct_indiv_sources',
            field=models.ManyToManyField(related_name='direct_source_agg_aggweeklynutritionr_reports', null=True, verbose_name='Primary. Sources (direct)', to='snisi_nutrition.WeeklyNutritionR', blank=True),
            preserve_default=True,
        ),
    ]
