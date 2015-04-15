# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('snisi_nutrition', '0007_auto_20141207_1054'),
    ]

    operations = [
        migrations.AlterField(
            model_name='aggnutritionr',
            name='agg_sources',
            field=models.ManyToManyField(related_name='aggregated_agg_aggnutritionr_reports', verbose_name='Aggr. Sources (all)', to='snisi_nutrition.AggNutritionR', blank=True),
        ),
        migrations.AlterField(
            model_name='aggnutritionr',
            name='direct_agg_sources',
            field=models.ManyToManyField(related_name='direct_aggregated_agg_aggnutritionr_reports', verbose_name='Aggr. Sources (direct)', to='snisi_nutrition.AggNutritionR', blank=True),
        ),
        migrations.AlterField(
            model_name='aggnutritionr',
            name='direct_indiv_sources',
            field=models.ManyToManyField(related_name='direct_source_agg_aggnutritionr_reports', verbose_name='Primary. Sources (direct)', to='snisi_nutrition.NutritionR', blank=True),
        ),
        migrations.AlterField(
            model_name='aggnutritionr',
            name='indiv_sources',
            field=models.ManyToManyField(related_name='source_agg_aggnutritionr_reports', verbose_name='Primary. Sources', to='snisi_nutrition.NutritionR', blank=True),
        ),
        migrations.AlterField(
            model_name='aggnutritionstocksr',
            name='agg_sources',
            field=models.ManyToManyField(related_name='aggregated_agg_aggnutritionstocksr_reports', verbose_name='Aggr. Sources (all)', to='snisi_nutrition.AggNutritionStocksR', blank=True),
        ),
        migrations.AlterField(
            model_name='aggnutritionstocksr',
            name='direct_agg_sources',
            field=models.ManyToManyField(related_name='direct_aggregated_agg_aggnutritionstocksr_reports', verbose_name='Aggr. Sources (direct)', to='snisi_nutrition.AggNutritionStocksR', blank=True),
        ),
        migrations.AlterField(
            model_name='aggnutritionstocksr',
            name='direct_indiv_sources',
            field=models.ManyToManyField(related_name='direct_source_agg_aggnutritionstocksr_reports', verbose_name='Primary. Sources (direct)', to='snisi_nutrition.NutritionStocksR', blank=True),
        ),
        migrations.AlterField(
            model_name='aggnutritionstocksr',
            name='indiv_sources',
            field=models.ManyToManyField(related_name='source_agg_aggnutritionstocksr_reports', verbose_name='Primary. Sources', to='snisi_nutrition.NutritionStocksR', blank=True),
        ),
        migrations.AlterField(
            model_name='aggurenamnutritionr',
            name='agg_sources',
            field=models.ManyToManyField(related_name='aggregated_agg_aggurenamnutritionr_reports', verbose_name='Aggr. Sources (all)', to='snisi_nutrition.AggURENAMNutritionR', blank=True),
        ),
        migrations.AlterField(
            model_name='aggurenamnutritionr',
            name='direct_agg_sources',
            field=models.ManyToManyField(related_name='direct_aggregated_agg_aggurenamnutritionr_reports', verbose_name='Aggr. Sources (direct)', to='snisi_nutrition.AggURENAMNutritionR', blank=True),
        ),
        migrations.AlterField(
            model_name='aggurenamnutritionr',
            name='direct_indiv_sources',
            field=models.ManyToManyField(related_name='direct_source_agg_aggurenamnutritionr_reports', verbose_name='Primary. Sources (direct)', to='snisi_nutrition.URENAMNutritionR', blank=True),
        ),
        migrations.AlterField(
            model_name='aggurenamnutritionr',
            name='indiv_sources',
            field=models.ManyToManyField(related_name='source_agg_aggurenamnutritionr_reports', verbose_name='Primary. Sources', to='snisi_nutrition.URENAMNutritionR', blank=True),
        ),
        migrations.AlterField(
            model_name='aggurenasnutritionr',
            name='agg_sources',
            field=models.ManyToManyField(related_name='aggregated_agg_aggurenasnutritionr_reports', verbose_name='Aggr. Sources (all)', to='snisi_nutrition.AggURENASNutritionR', blank=True),
        ),
        migrations.AlterField(
            model_name='aggurenasnutritionr',
            name='direct_agg_sources',
            field=models.ManyToManyField(related_name='direct_aggregated_agg_aggurenasnutritionr_reports', verbose_name='Aggr. Sources (direct)', to='snisi_nutrition.AggURENASNutritionR', blank=True),
        ),
        migrations.AlterField(
            model_name='aggurenasnutritionr',
            name='direct_indiv_sources',
            field=models.ManyToManyField(related_name='direct_source_agg_aggurenasnutritionr_reports', verbose_name='Primary. Sources (direct)', to='snisi_nutrition.URENASNutritionR', blank=True),
        ),
        migrations.AlterField(
            model_name='aggurenasnutritionr',
            name='indiv_sources',
            field=models.ManyToManyField(related_name='source_agg_aggurenasnutritionr_reports', verbose_name='Primary. Sources', to='snisi_nutrition.URENASNutritionR', blank=True),
        ),
        migrations.AlterField(
            model_name='aggureninutritionr',
            name='agg_sources',
            field=models.ManyToManyField(related_name='aggregated_agg_aggureninutritionr_reports', verbose_name='Aggr. Sources (all)', to='snisi_nutrition.AggURENINutritionR', blank=True),
        ),
        migrations.AlterField(
            model_name='aggureninutritionr',
            name='direct_agg_sources',
            field=models.ManyToManyField(related_name='direct_aggregated_agg_aggureninutritionr_reports', verbose_name='Aggr. Sources (direct)', to='snisi_nutrition.AggURENINutritionR', blank=True),
        ),
        migrations.AlterField(
            model_name='aggureninutritionr',
            name='direct_indiv_sources',
            field=models.ManyToManyField(related_name='direct_source_agg_aggureninutritionr_reports', verbose_name='Primary. Sources (direct)', to='snisi_nutrition.URENINutritionR', blank=True),
        ),
        migrations.AlterField(
            model_name='aggureninutritionr',
            name='indiv_sources',
            field=models.ManyToManyField(related_name='source_agg_aggureninutritionr_reports', verbose_name='Primary. Sources', to='snisi_nutrition.URENINutritionR', blank=True),
        ),
        migrations.AlterField(
            model_name='aggweeklynutritionr',
            name='agg_sources',
            field=models.ManyToManyField(related_name='aggregated_agg_aggweeklynutritionr_reports', verbose_name='Aggr. Sources (all)', to='snisi_nutrition.AggWeeklyNutritionR', blank=True),
        ),
        migrations.AlterField(
            model_name='aggweeklynutritionr',
            name='direct_agg_sources',
            field=models.ManyToManyField(related_name='direct_aggregated_agg_aggweeklynutritionr_reports', verbose_name='Aggr. Sources (direct)', to='snisi_nutrition.AggWeeklyNutritionR', blank=True),
        ),
        migrations.AlterField(
            model_name='aggweeklynutritionr',
            name='direct_indiv_sources',
            field=models.ManyToManyField(related_name='direct_source_agg_aggweeklynutritionr_reports', verbose_name='Primary. Sources (direct)', to='snisi_nutrition.WeeklyNutritionR', blank=True),
        ),
        migrations.AlterField(
            model_name='aggweeklynutritionr',
            name='indiv_sources',
            field=models.ManyToManyField(related_name='source_agg_aggweeklynutritionr_reports', verbose_name='Primary. Sources', to='snisi_nutrition.WeeklyNutritionR', blank=True),
        ),
    ]
