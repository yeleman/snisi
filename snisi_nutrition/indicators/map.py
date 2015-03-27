#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim: ai ts=4 sts=4 et sw=4 nu

from __future__ import (unicode_literals, absolute_import,
                        division, print_function)
import logging

from snisi_core.indicators import (
    IndicatorTable, em, SummaryForEntitiesTable, ReportDataMixin,
    DataIsMissing, yAxis, serie_type)
from snisi_nutrition.indicators.common import (
    IndicatorTableWithEntities, NumberOfHealthUnitsReporting,
    NutritionIndicator, shoudl_show, gen_fixed_entity_indicator)

logger = logging.getLogger(__name__)


class HealthUnitsWithStockout(NutritionIndicator):
    is_ratio = True
    geo_section = "Intrants"
    is_yesno = True
    sub_func_name = None
    sub_func_params = []

    def _compute(self):
        if self.is_hc():
            return getattr(self.report.stocks_report,
                           self.sub_func_name)(*self.sub_func_params)
        nb_stockout = sum(
            [bool(v)
             for v in self.all_hc_func_values('stocks_report',
                                              self.sub_func_name,
                                              *self.sub_func_params)])
        return self.divide(nb_stockout,
                           NumberOfHealthUnitsReporting.clone_from(self).data)


class HealthUnitsWithInputsStockout(HealthUnitsWithStockout):
    name = "Structures avec rupture de stocks en intrants"
    sub_func_name = 'has_stockout'
    is_geo_friendly = True


class HealthUnitsWithTherapeuticInputsStockout(HealthUnitsWithStockout):
    name = "Structures avec rupture de stocks en intrants thérapeutique"
    sub_func_name = 'has_therapeutic_stockout'
    is_geo_friendly = True


class HealthUnitsWithDrugInputsStockout(HealthUnitsWithStockout):
    name = "Structures avec rupture de stocks en médicaments"
    sub_func_name = 'has_drug_stockout'
    is_geo_friendly = True


class HealthUnitsWithPlumpyNutStockout(HealthUnitsWithStockout):
    name = "Structures avec rupture de stocks: Plumpy Nut"
    sub_func_name = 'has_stockout_from'
    is_geo_friendly = True
    sub_func_params = [['plumpy_nut']]


class HealthUnitsWithMilkF75Stockout(HealthUnitsWithStockout):
    name = "Structures avec rupture de stocks: Lait F75"
    sub_func_name = 'has_stockout_from'
    is_geo_friendly = True
    sub_func_params = [['milk_f75']]


class HealthUnitsWithMilkF100Stockout(HealthUnitsWithStockout):
    name = "Structures avec rupture de stocks: Lait F100"
    sub_func_name = 'has_stockout_from'
    is_geo_friendly = True
    sub_func_params = [['milk_f100']]


class HealthUnitsWithPlumpySupStockout(HealthUnitsWithStockout):
    name = "Structures avec rupture de stocks: Plumpy Sup"
    sub_func_name = 'has_stockout_from'
    is_geo_friendly = True
    sub_func_params = [['plumpy_sup']]


class HealthUnitsWithSupercerealStockout(HealthUnitsWithStockout):
    name = "Structures avec rupture de stocks: Supercereal"
    sub_func_name = 'has_stockout_from'
    is_geo_friendly = True
    sub_func_params = [['supercereal']]


class HealthUnitsWithSupercerealPlusStockout(HealthUnitsWithStockout):
    name = "Structures avec rupture de stocks: Supercereal+"
    sub_func_name = 'has_stockout_from'
    is_geo_friendly = True
    sub_func_params = [['supercereal_plus']]


class HealthUnitsWithOilStockout(HealthUnitsWithStockout):
    name = "Structures avec rupture de stocks: Huile"
    sub_func_name = 'has_stockout_from'
    is_geo_friendly = True
    sub_func_params = [['oil']]


class HealthUnitsWithAmoxycilline125VialsStockout(HealthUnitsWithStockout):
    name = "Structures avec rupture de stocks: Amoxycilline 125"
    sub_func_name = 'has_stockout_from'
    is_geo_friendly = True
    sub_func_params = [['amoxycilline_125_vials']]


class HealthUnitsWithAmoxycilline250CapsStockout(HealthUnitsWithStockout):
    name = "Structures avec rupture de stocks: Amoxycilline 250"
    sub_func_name = 'has_stockout_from'
    is_geo_friendly = True
    sub_func_params = [['amoxycilline_250_caps']]


class HealthUnitsWithAlbendazoleStockout(HealthUnitsWithStockout):
    name = "Structures avec rupture de stocks: Albendazole"
    sub_func_name = 'has_stockout_from'
    is_geo_friendly = True
    sub_func_params = [['albendazole_400']]


class HealthUnitsWithVitaminA100Stockout(HealthUnitsWithStockout):
    name = "Structures avec rupture de stocks: Vitamin A 100"
    sub_func_name = 'has_stockout_from'
    is_geo_friendly = True
    sub_func_params = [['vita_100_injectable']]


class HealthUnitsWithVitaminA200Stockout(HealthUnitsWithStockout):
    name = "Structures avec rupture de stocks: Vitamin A 200"
    sub_func_name = 'has_stockout_from'
    is_geo_friendly = True
    sub_func_params = [['vita_200_injectable']]


class HealthUnitsWithIronFolicAcidStockout(HealthUnitsWithStockout):
    name = "Structures avec rupture de stocks: Iron/Folic Acid"
    sub_func_name = 'has_stockout_from'
    is_geo_friendly = True
    sub_func_params = [['iron_folic_acid']]
