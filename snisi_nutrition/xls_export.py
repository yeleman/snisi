#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim: ai ts=4 sts=4 et sw=4 nu

from __future__ import (unicode_literals, absolute_import,
                        division, print_function)
import logging
import StringIO
import os

from xlrd import open_workbook
from xlutils.copy import copy

from snisi_core.xls_export import xls_update_value_only
from snisi_reprohealth import get_domain

from snisi_nutrition.models.URENAM import URENAMNutritionR
from snisi_nutrition.models.URENAS import URENASNutritionR
from snisi_nutrition.models.URENI import URENINutritionR
from snisi_nutrition.models.Stocks import NutritionStocksR

logger = logging.getLogger(__name__)


def pfa_activities_as_xls(report):
    """ Export les données d'un rapport en xls """

    template_path = os.path.join(get_domain().module_path,
                                 'fixtures', 'template-nutrition.xls')

    template = open_workbook(template_path, formatting_info=True)
    copy_week_b = copy(template)
    sheet_STOCKS = copy_week_b.get_sheet(0)
    sheet_STOCKS.portrait = False
    sheet_URENAMURENAS = copy_week_b.get_sheet(1)
    sheet_URENAMURENAS.portrait = False
    sheet_URENI = copy_week_b.get_sheet(2)
    sheet_URENI.portrait = False
    del(template)

    xls_update_value_only(sheet_STOCKS, 1, 3,
                          report.entity.name)
    xls_update_value_only(sheet_STOCKS, 1, 4,
                          report.entity.slug)
    xls_update_value_only(sheet_STOCKS, 5, 2,
                          report.period.middle().month)
    xls_update_value_only(sheet_STOCKS, 5, 3,
                          report.period.middle().year)

    # STOCKS
    xls_update_value_only(sheet_URENAM, 3, 7, URENAMNutritionR.plumpy_nut_initial)
    xls_update_value_only(sheet_URENAM, 5, 7, URENAMNutritionR.plumpy_nut_received)
    xls_update_value_only(sheet_URENAM, 7, 7, URENAMNutritionR.plumpy_nut_used)
    xls_update_value_only(sheet_URENAM, 9, 7, URENAMNutritionR.plumpy_nut_lost)
    xls_update_value_only(sheet_URENAM, 3, 8, URENAMNutritionR.milk_f75_initial)
    xls_update_value_only(sheet_URENAM, 5, 8, URENAMNutritionR.milk_f75_received)
    xls_update_value_only(sheet_URENAM, 7, 8, URENAMNutritionR.milk_f75_used)
    xls_update_value_only(sheet_URENAM, 9, 8, URENAMNutritionR.milk_f75_lost)
    xls_update_value_only(sheet_URENAM, 3, 9, URENAMNutritionR.milk_f100_initial)
    xls_update_value_only(sheet_URENAM, 5, 9, URENAMNutritionR.milk_f100_received)
    xls_update_value_only(sheet_URENAM, 7, 9, URENAMNutritionR.milk_f100_used)
    xls_update_value_only(sheet_URENAM, 9, 9, URENAMNutritionR.milk_f100_lost)
    xls_update_value_only(sheet_URENAM, 3, 10, URENAMNutritionR.resomal_initial)
    xls_update_value_only(sheet_URENAM, 5, 10, URENAMNutritionR.resomal_received)
    xls_update_value_only(sheet_URENAM, 7, 10, URENAMNutritionR.resomal_used)
    xls_update_value_only(sheet_URENAM, 9, 10, URENAMNutritionR.resomal_lost)
    xls_update_value_only(sheet_URENAM, 3, 11, URENAMNutritionR.plumpy_sup_initial)
    xls_update_value_only(sheet_URENAM, 5, 11, URENAMNutritionR.plumpy_sup_received)
    xls_update_value_only(sheet_URENAM, 7, 11, URENAMNutritionR.plumpy_sup_used)
    xls_update_value_only(sheet_URENAM, 9, 11, URENAMNutritionR.plumpy_sup_lost)
    xls_update_value_only(sheet_URENAM, 3, 12, URENAMNutritionR.supercereal_initial)
    xls_update_value_only(sheet_URENAM, 5, 12, URENAMNutritionR.supercereal_received)
    xls_update_value_only(sheet_URENAM, 7, 12, URENAMNutritionR.supercereal_used)
    xls_update_value_only(sheet_URENAM, 9, 12, URENAMNutritionR.supercereal_lost)
    xls_update_value_only(sheet_URENAM, 3, 13, URENAMNutritionR.supercereal_plus_initial)
    xls_update_value_only(sheet_URENAM, 5, 13, URENAMNutritionR.supercereal_plus_received)
    xls_update_value_only(sheet_URENAM, 7, 13, URENAMNutritionR.supercereal_plus_used)
    xls_update_value_only(sheet_URENAM, 9, 13, URENAMNutritionR.supercereal_plus_lost)
    xls_update_value_only(sheet_URENAM, 3, 14, URENAMNutritionR.oil_initial)
    xls_update_value_only(sheet_URENAM, 5, 14, URENAMNutritionR.oil_received)
    xls_update_value_only(sheet_URENAM, 7, 14, URENAMNutritionR.oil_used)
    xls_update_value_only(sheet_URENAM, 9, 14, URENAMNutritionR.oil_lost)
    xls_update_value_only(sheet_URENAM, 3, 15, URENAMNutritionR.amoxycilline_125_vials_initial)
    xls_update_value_only(sheet_URENAM, 5, 15, URENAMNutritionR.amoxycilline_125_vials_received)
    xls_update_value_only(sheet_URENAM, 7, 15, URENAMNutritionR.amoxycilline_125_vials_used)
    xls_update_value_only(sheet_URENAM, 9, 15, URENAMNutritionR.amoxycilline_125_vials_lost)
    xls_update_value_only(sheet_URENAM, 3, 16, URENAMNutritionR.amoxycilline_250_caps_initial)
    xls_update_value_only(sheet_URENAM, 5, 16, URENAMNutritionR.amoxycilline_250_caps_received)
    xls_update_value_only(sheet_URENAM, 7, 16, URENAMNutritionR.amoxycilline_250_caps_used)
    xls_update_value_only(sheet_URENAM, 9, 16, URENAMNutritionR.amoxycilline_250_caps_lost)
    xls_update_value_only(sheet_URENAM, 3, 17, URENAMNutritionR.albendazole_400_initial)
    xls_update_value_only(sheet_URENAM, 5, 17, URENAMNutritionR.albendazole_400_received)
    xls_update_value_only(sheet_URENAM, 7, 17, URENAMNutritionR.albendazole_400_used)
    xls_update_value_only(sheet_URENAM, 9, 17, URENAMNutritionR.albendazole_400_lost)
    xls_update_value_only(sheet_URENAM, 3, 18, URENAMNutritionR.vita_100_injectable_initial)
    xls_update_value_only(sheet_URENAM, 5, 18, URENAMNutritionR.vita_100_injectable_received)
    xls_update_value_only(sheet_URENAM, 7, 18, URENAMNutritionR.vita_100_injectable_used)
    xls_update_value_only(sheet_URENAM, 9, 18, URENAMNutritionR.vita_100_injectable_lost)
    xls_update_value_only(sheet_URENAM, 3, 19, URENAMNutritionR.vita_200_injectable_initial)
    xls_update_value_only(sheet_URENAM, 5, 19, URENAMNutritionR.vita_200_injectable_received)
    xls_update_value_only(sheet_URENAM, 7, 19, URENAMNutritionR.vita_200_injectable_used)
    xls_update_value_only(sheet_URENAM, 9, 19, URENAMNutritionR.vita_200_injectable_lost)
    xls_update_value_only(sheet_URENAM, 3, 20, URENAMNutritionR.iron_folic_acid_initial)
    xls_update_value_only(sheet_URENAM, 5, 20, URENAMNutritionR.iron_folic_acid_received)
    xls_update_value_only(sheet_URENAM, 7, 20, URENAMNutritionR.iron_folic_acid_used)
    xls_update_value_only(sheet_URENAM, 9, 20, URENAMNutritionR.iron_folic_acid_lost)
    
    # URENAM
    xls_update_value_only(sheet_STOCKS, 2, 14, NutritionStocksR.u23o6_total_start_m)
    xls_update_value_only(sheet_STOCKS, 3, 14, NutritionStocksR.u23o6_total_start_f)
    xls_update_value_only(sheet_STOCKS, 4, 14, NutritionStocksR.u23o6_new_cases)
    xls_update_value_only(sheet_STOCKS, 7, 14, NutritionStocksR.u23o6_returned)
    xls_update_value_only(sheet_STOCKS, 11, 14, NutritionStocksR.u23o6_total_in_m)
    xls_update_value_only(sheet_STOCKS, 12, 14, NutritionStocksR.u23o6_total_in_f)
    xls_update_value_only(sheet_STOCKS, 1, 29, NutritionStocksR.u23o6_healed)
    xls_update_value_only(sheet_STOCKS, 3, 29, NutritionStocksR.u23o6_deceased)
    xls_update_value_only(sheet_STOCKS, 5, 29, NutritionStocksR.u23o6_abandon)
    xls_update_value_only(sheet_STOCKS, 7, 29, NutritionStocksR.u23o6_not_responding)
    xls_update_value_only(sheet_STOCKS, 10, 29, NutritionStocksR.u23o6_total_out_m)
    xls_update_value_only(sheet_STOCKS, 11, 29, NutritionStocksR.u23o6_total_out_f)
    xls_update_value_only(sheet_STOCKS, 12, 29, NutritionStocksR.u23o6_referred)
    xls_update_value_only(sheet_STOCKS, 16, 29, NutritionStocksR.u23o6_total_end_m)
    xls_update_value_only(sheet_STOCKS, 17, 29, NutritionStocksR.u23o6_total_end_f)
    xls_update_value_only(sheet_STOCKS, 2, 15, NutritionStocksR.u59o23_total_start_m)
    xls_update_value_only(sheet_STOCKS, 3, 15, NutritionStocksR.u59o23_total_start_f)
    xls_update_value_only(sheet_STOCKS, 4, 15, NutritionStocksR.u59o23_new_cases)
    xls_update_value_only(sheet_STOCKS, 7, 15, NutritionStocksR.u59o23_returned)
    xls_update_value_only(sheet_STOCKS, 11, 15, NutritionStocksR.u59o23_total_in_m)
    xls_update_value_only(sheet_STOCKS, 12, 15, NutritionStocksR.u59o23_total_in_f)
    xls_update_value_only(sheet_STOCKS, 1, 30, NutritionStocksR.u59o23_healed)
    xls_update_value_only(sheet_STOCKS, 3, 30, NutritionStocksR.u59o23_deceased)
    xls_update_value_only(sheet_STOCKS, 5, 30, NutritionStocksR.u59o23_abandon)
    xls_update_value_only(sheet_STOCKS, 7, 30, NutritionStocksR.u59o23_not_responding)
    xls_update_value_only(sheet_STOCKS, 10, 30, NutritionStocksR.u59o23_total_out_m)
    xls_update_value_only(sheet_STOCKS, 11, 30, NutritionStocksR.u59o23_total_out_f)
    xls_update_value_only(sheet_STOCKS, 12, 30, NutritionStocksR.u59o23_referred)
    xls_update_value_only(sheet_STOCKS, 16, 30, NutritionStocksR.u59o23_total_end_m)
    xls_update_value_only(sheet_STOCKS, 17, 30, NutritionStocksR.u59o23_total_end_f)
    xls_update_value_only(sheet_STOCKS, 2, 16, NutritionStocksR.o59_total_start_m)
    xls_update_value_only(sheet_STOCKS, 3, 16, NutritionStocksR.o59_total_start_f)
    xls_update_value_only(sheet_STOCKS, 4, 16, NutritionStocksR.o59_new_cases)
    xls_update_value_only(sheet_STOCKS, 7, 16, NutritionStocksR.o59_returned)
    xls_update_value_only(sheet_STOCKS, 11, 16, NutritionStocksR.o59_total_in_m)
    xls_update_value_only(sheet_STOCKS, 12, 16, NutritionStocksR.o59_total_in_f)
    xls_update_value_only(sheet_STOCKS, 1, 31, NutritionStocksR.o59_healed)
    xls_update_value_only(sheet_STOCKS, 3, 31, NutritionStocksR.o59_deceased)
    xls_update_value_only(sheet_STOCKS, 5, 31, NutritionStocksR.o59_abandon)
    xls_update_value_only(sheet_STOCKS, 7, 31, NutritionStocksR.o59_not_responding)
    xls_update_value_only(sheet_STOCKS, 10, 31, NutritionStocksR.o59_total_out_m)
    xls_update_value_only(sheet_STOCKS, 11, 31, NutritionStocksR.o59_total_out_f)
    xls_update_value_only(sheet_STOCKS, 12, 31, NutritionStocksR.o59_referred)
    xls_update_value_only(sheet_STOCKS, 16, 31, NutritionStocksR.o59_total_end_m)
    xls_update_value_only(sheet_STOCKS, 17, 31, NutritionStocksR.o59_total_end_f)
    xls_update_value_only(sheet_STOCKS, 3, 17, NutritionStocksR.pw_total_start_f)
    xls_update_value_only(sheet_STOCKS, 4, 17, NutritionStocksR.pw_new_cases)
    xls_update_value_only(sheet_STOCKS, 7, 17, NutritionStocksR.pw_returned)
    xls_update_value_only(sheet_STOCKS, 12, 17, NutritionStocksR.pw_total_in_f)
    xls_update_value_only(sheet_STOCKS, 1, 32, NutritionStocksR.pw_healed)
    xls_update_value_only(sheet_STOCKS, 3, 32, NutritionStocksR.pw_deceased)
    xls_update_value_only(sheet_STOCKS, 5, 32, NutritionStocksR.pw_abandon)
    xls_update_value_only(sheet_STOCKS, 7, 32, NutritionStocksR.pw_not_responding)
    xls_update_value_only(sheet_STOCKS, 11, 32, NutritionStocksR.pw_total_out_f)
    xls_update_value_only(sheet_STOCKS, 12, 32, NutritionStocksR.pw_referred)
    xls_update_value_only(sheet_STOCKS, 17, 32, NutritionStocksR.pw_total_end_f)
    xls_update_value_only(sheet_STOCKS, 2, 18, NutritionStocksR.exsam_total_start_m)
    xls_update_value_only(sheet_STOCKS, 3, 18, NutritionStocksR.exsam_total_start_f)
    xls_update_value_only(sheet_STOCKS, 12, 33, NutritionStocksR.exsam_referred)
    xls_update_value_only(sheet_STOCKS, 16, 33, NutritionStocksR.exsam_total_end_m)
    xls_update_value_only(sheet_STOCKS, 17, 33, NutritionStocksR.exsam_total_end_f)

    # URENAS
    xls_update_value_only(sheet_URENAS, 2, 10, URENASNutritionR.u59o6_total_start_m)
    xls_update_value_only(sheet_URENAS, 3, 10, URENASNutritionR.u59o6_total_start_f)
    xls_update_value_only(sheet_URENAS, 4, 10, URENASNutritionR.u59o6_new_cases)
    xls_update_value_only(sheet_URENAS, 7, 10, URENASNutritionR.u59o6_returned)
    xls_update_value_only(sheet_URENAS, 11, 10, URENASNutritionR.u59o6_total_in_m)
    xls_update_value_only(sheet_URENAS, 12, 10, URENASNutritionR.u59o6_total_in_f)
    xls_update_value_only(sheet_URENAS, 13, 10, URENASNutritionR.u59o6_transferred)
    xls_update_value_only(sheet_URENAS, 1, 25, URENASNutritionR.u59o6_healed)
    xls_update_value_only(sheet_URENAS, 3, 25, URENASNutritionR.u59o6_deceased)
    xls_update_value_only(sheet_URENAS, 5, 25, URENASNutritionR.u59o6_abandon)
    xls_update_value_only(sheet_URENAS, 7, 25, URENASNutritionR.u59o6_not_responding)
    xls_update_value_only(sheet_URENAS, 10, 25, URENASNutritionR.u59o6_total_out_m)
    xls_update_value_only(sheet_URENAS, 11, 25, URENASNutritionR.u59o6_total_out_f)
    xls_update_value_only(sheet_URENAS, 12, 25, URENASNutritionR.u59o6_referred)
    xls_update_value_only(sheet_URENAS, 16, 25, URENASNutritionR.u59o6_total_end_m)
    xls_update_value_only(sheet_URENAS, 17, 25, URENASNutritionR.u59o6_total_end_f)
    xls_update_value_only(sheet_URENAS, 2, 11, URENASNutritionR.o59_total_start_m)
    xls_update_value_only(sheet_URENAS, 3, 11, URENASNutritionR.o59_total_start_f)
    xls_update_value_only(sheet_URENAS, 4, 11, URENASNutritionR.o59_new_cases)
    xls_update_value_only(sheet_URENAS, 7, 11, URENASNutritionR.o59_returned)
    xls_update_value_only(sheet_URENAS, 11, 11, URENASNutritionR.o59_total_in_m)
    xls_update_value_only(sheet_URENAS, 12, 11, URENASNutritionR.o59_total_in_f)
    xls_update_value_only(sheet_URENAS, 13, 11, URENASNutritionR.o59_transferred)
    xls_update_value_only(sheet_URENAS, 1, 26, URENASNutritionR.o59_healed)
    xls_update_value_only(sheet_URENAS, 3, 26, URENASNutritionR.o59_deceased)
    xls_update_value_only(sheet_URENAS, 5, 26, URENASNutritionR.o59_abandon)
    xls_update_value_only(sheet_URENAS, 7, 26, URENASNutritionR.o59_not_responding)
    xls_update_value_only(sheet_URENAS, 10, 26, URENASNutritionR.o59_total_out_m)
    xls_update_value_only(sheet_URENAS, 11, 26, URENASNutritionR.o59_total_out_f)
    xls_update_value_only(sheet_URENAS, 12, 26, URENASNutritionR.o59_referred)
    xls_update_value_only(sheet_URENAS, 16, 26, URENASNutritionR.o59_total_end_m)
    xls_update_value_only(sheet_URENAS, 17, 26, URENASNutritionR.o59_total_end_f)

    # URENI
    xls_update_value_only(sheet_URENI, 2, 10, URENINutritionR.u6_total_start_m)
    xls_update_value_only(sheet_URENI, 3, 10, URENINutritionR.u6_total_start_f)
    xls_update_value_only(sheet_URENI, 4, 10, URENINutritionR.u6_new_cases)
    xls_update_value_only(sheet_URENI, 7, 10, URENINutritionR.u6_returned)
    xls_update_value_only(sheet_URENI, 11, 10, URENINutritionR.u6_total_in_m)
    xls_update_value_only(sheet_URENI, 12, 10, URENINutritionR.u6_total_in_f)
    xls_update_value_only(sheet_URENI, 13, 10, URENINutritionR.u6_transferred)
    xls_update_value_only(sheet_URENI, 1, 19, URENINutritionR.u6_healed)
    xls_update_value_only(sheet_URENI, 3, 19, URENINutritionR.u6_deceased)
    xls_update_value_only(sheet_URENI, 5, 19, URENINutritionR.u6_abandon)
    xls_update_value_only(sheet_URENI, 7, 19, URENINutritionR.u6_not_responding)
    xls_update_value_only(sheet_URENI, 10, 19, URENINutritionR.u6_total_out_m)
    xls_update_value_only(sheet_URENI, 11, 19, URENINutritionR.u6_total_out_f)
    xls_update_value_only(sheet_URENI, 12, 19, URENINutritionR.u6_referred)
    xls_update_value_only(sheet_URENI, 16, 19, URENINutritionR.u6_total_end_m)
    xls_update_value_only(sheet_URENI, 17, 19, URENINutritionR.u6_total_end_f)
    xls_update_value_only(sheet_URENI, 2, 11, URENINutritionR.u59o6_total_start_m)
    xls_update_value_only(sheet_URENI, 3, 11, URENINutritionR.u59o6_total_start_f)
    xls_update_value_only(sheet_URENI, 4, 11, URENINutritionR.u59o6_new_cases)
    xls_update_value_only(sheet_URENI, 7, 11, URENINutritionR.u59o6_returned)
    xls_update_value_only(sheet_URENI, 11, 11, URENINutritionR.u59o6_total_in_m)
    xls_update_value_only(sheet_URENI, 12, 11, URENINutritionR.u59o6_total_in_f)
    xls_update_value_only(sheet_URENI, 13, 11, URENINutritionR.u59o6_transferred)
    xls_update_value_only(sheet_URENI, 1, 20, URENINutritionR.u59o6_healed)
    xls_update_value_only(sheet_URENI, 3, 20, URENINutritionR.u59o6_deceased)
    xls_update_value_only(sheet_URENI, 5, 20, URENINutritionR.u59o6_abandon)
    xls_update_value_only(sheet_URENI, 7, 20, URENINutritionR.u59o6_not_responding)
    xls_update_value_only(sheet_URENI, 10, 20, URENINutritionR.u59o6_total_out_m)
    xls_update_value_only(sheet_URENI, 11, 20, URENINutritionR.u59o6_total_out_f)
    xls_update_value_only(sheet_URENI, 12, 20, URENINutritionR.u59o6_referred)
    xls_update_value_only(sheet_URENI, 16, 20, URENINutritionR.u59o6_total_end_m)
    xls_update_value_only(sheet_URENI, 17, 20, URENINutritionR.u59o6_total_end_f)
    xls_update_value_only(sheet_URENI, 2, 12, URENINutritionR.o59_total_start_m)
    xls_update_value_only(sheet_URENI, 3, 12, URENINutritionR.o59_total_start_f)
    xls_update_value_only(sheet_URENI, 4, 12, URENINutritionR.o59_new_cases)
    xls_update_value_only(sheet_URENI, 7, 12, URENINutritionR.o59_returned)
    xls_update_value_only(sheet_URENI, 11, 12, URENINutritionR.o59_total_in_m)
    xls_update_value_only(sheet_URENI, 12, 12, URENINutritionR.o59_total_in_f)
    xls_update_value_only(sheet_URENI, 13, 12, URENINutritionR.o59_transferred)
    xls_update_value_only(sheet_URENI, 1, 21, URENINutritionR.o59_healed)
    xls_update_value_only(sheet_URENI, 3, 21, URENINutritionR.o59_deceased)
    xls_update_value_only(sheet_URENI, 5, 21, URENINutritionR.o59_abandon)
    xls_update_value_only(sheet_URENI, 7, 21, URENINutritionR.o59_not_responding)
    xls_update_value_only(sheet_URENI, 10, 21, URENINutritionR.o59_total_out_m)
    xls_update_value_only(sheet_URENI, 11, 21, URENINutritionR.o59_total_out_f)
    xls_update_value_only(sheet_URENI, 12, 21, URENINutritionR.o59_referred)
    xls_update_value_only(sheet_URENI, 16, 21, URENINutritionR.o59_total_end_m)
    xls_update_value_only(sheet_URENI, 17, 21, URENINutritionR.o59_total_end_f)

    stream = StringIO.StringIO()
    copy_week_b.save(stream)

    return stream
