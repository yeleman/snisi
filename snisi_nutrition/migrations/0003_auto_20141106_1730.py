# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('snisi_nutrition', '0002_auto_20141104_1734'),
    ]

    operations = [
        migrations.AddField(
            model_name='aggnutritionr',
            name='stocks_report',
            field=models.ForeignKey(related_name='agg_nutritionr', blank=True, to='snisi_nutrition.AggNutritionStocksR', null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='nutritionr',
            name='stocks_report',
            field=models.ForeignKey(related_name='nutritionr', blank=True, to='snisi_nutrition.NutritionStocksR', null=True),
            preserve_default=True,
        ),
    ]
