#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim: ai ts=4 sts=4 et sw=4 nu

from __future__ import (unicode_literals, absolute_import,
                        division, print_function)
import logging

from django.contrib import admin
from snisi_core.admin import ReportAdmin
from snisi_nutrition.models.Monthly import NutritionR, AggNutritionR
from snisi_nutrition.models.URENAS import (
    URENASNutritionR, AggURENASNutritionR)
from snisi_nutrition.models.URENAM import (
    URENAMNutritionR, AggURENAMNutritionR)
from snisi_nutrition.models.URENI import (
    URENINutritionR, AggURENINutritionR)
from snisi_nutrition.models.Stocks import (
    NutritionStocksR, AggNutritionStocksR)
from snisi_nutrition.models.Weekly import (
    WeeklyNutritionR, AggWeeklyNutritionR)

logger = logging.getLogger(__name__)

admin.site.register(NutritionR, ReportAdmin)
admin.site.register(AggNutritionR, ReportAdmin)
admin.site.register(URENASNutritionR, ReportAdmin)
admin.site.register(AggURENASNutritionR, ReportAdmin)
admin.site.register(URENAMNutritionR, ReportAdmin)
admin.site.register(AggURENAMNutritionR, ReportAdmin)
admin.site.register(URENINutritionR, ReportAdmin)
admin.site.register(AggURENINutritionR, ReportAdmin)
admin.site.register(NutritionStocksR, ReportAdmin)
admin.site.register(AggNutritionStocksR, ReportAdmin)
admin.site.register(WeeklyNutritionR, ReportAdmin)
admin.site.register(AggWeeklyNutritionR, ReportAdmin)
