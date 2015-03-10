#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim: ai ts=4 sts=4 et sw=4 nu

from __future__ import (unicode_literals, absolute_import,
                        division, print_function)
import logging
import StringIO
import os
import copy

from py3compat import text_type
import xlwt
from xlrd import open_workbook
from xlutils.copy import copy as xl_copy

from snisi_core.xls_export import xls_update_value_only
from snisi_nutrition import get_domain
from snisi_tools.datetime import get_periods_str

logger = logging.getLogger(__name__)


def nutrition_monthly_as_xls(report):
    """ Export les données d'un rapport en xls """

    template_path = os.path.join(get_domain().module_path,
                                 'fixtures', 'template-nutrition.xls')

    template = open_workbook(template_path, formatting_info=True)
    copy_week_b = xl_copy(template)
    sheet_STOCKS = copy_week_b.get_sheet(0)
    sheet_STOCKS.portrait = False
    sheet_URENAMURENAS = copy_week_b.get_sheet(1)
    sheet_URENAMURENAS.portrait = False
    sheet_URENI = copy_week_b.get_sheet(2)
    sheet_URENI.portrait = False
    del(template)

    entity = report.entity.casted()

    meta_map = [
        (sheet_STOCKS, 1, 5),
        (sheet_URENAMURENAS, 5, 14),
        (sheet_URENI, 5, 14),
    ]

    for sheet, colA, colB in meta_map:
        if entity.type.slug in ('health_region',
                                'health_district',
                                'health_center'):
            xls_update_value_only(sheet, colA, 2,
                                  entity.get_health_region().name)
        if entity.type.slug in ('health_district', 'health_center'):
            xls_update_value_only(sheet, colA, 3,
                                  entity.get_health_district().name)
        xls_update_value_only(sheet, colA, 4, report.entity.slug)
        xls_update_value_only(sheet, colB, 2, report.period.middle().month)
        xls_update_value_only(sheet, colB, 3, report.period.middle().year)
        xls_update_value_only(sheet, colB, 4,
                              report.created_by.get_title_full_name())

    # STOCKS
    xls_update_value_only(sheet_STOCKS, 3, 7,
                          report.stocks_report.plumpy_nut_initial)
    xls_update_value_only(sheet_STOCKS, 5, 7,
                          report.stocks_report.plumpy_nut_received)
    xls_update_value_only(sheet_STOCKS, 7, 7,
                          report.stocks_report.plumpy_nut_used)
    xls_update_value_only(sheet_STOCKS, 9, 7,
                          report.stocks_report.plumpy_nut_lost)
    xls_update_value_only(sheet_STOCKS, 11, 7,
                          report.stocks_report.plumpy_nut_balance)
    xls_update_value_only(sheet_STOCKS, 3, 8,
                          report.stocks_report.milk_f75_initial)
    xls_update_value_only(sheet_STOCKS, 5, 8,
                          report.stocks_report.milk_f75_received)
    xls_update_value_only(sheet_STOCKS, 7, 8,
                          report.stocks_report.milk_f75_used)
    xls_update_value_only(sheet_STOCKS, 9, 8,
                          report.stocks_report.milk_f75_lost)
    xls_update_value_only(sheet_STOCKS, 11, 8,
                          report.stocks_report.milk_f75_balance)
    xls_update_value_only(sheet_STOCKS, 3, 9,
                          report.stocks_report.milk_f100_initial)
    xls_update_value_only(sheet_STOCKS, 5, 9,
                          report.stocks_report.milk_f100_received)
    xls_update_value_only(sheet_STOCKS, 7, 9,
                          report.stocks_report.milk_f100_used)
    xls_update_value_only(sheet_STOCKS, 9, 9,
                          report.stocks_report.milk_f100_lost)
    xls_update_value_only(sheet_STOCKS, 11, 9,
                          report.stocks_report.milk_f100_balance)
    xls_update_value_only(sheet_STOCKS, 3, 10,
                          report.stocks_report.resomal_initial)
    xls_update_value_only(sheet_STOCKS, 5, 10,
                          report.stocks_report.resomal_received)
    xls_update_value_only(sheet_STOCKS, 7, 10,
                          report.stocks_report.resomal_used)
    xls_update_value_only(sheet_STOCKS, 9, 10,
                          report.stocks_report.resomal_lost)
    xls_update_value_only(sheet_STOCKS, 11, 10,
                          report.stocks_report.resomal_balance)
    xls_update_value_only(sheet_STOCKS, 3, 11,
                          report.stocks_report.plumpy_sup_initial)
    xls_update_value_only(sheet_STOCKS, 5, 11,
                          report.stocks_report.plumpy_sup_received)
    xls_update_value_only(sheet_STOCKS, 7, 11,
                          report.stocks_report.plumpy_sup_used)
    xls_update_value_only(sheet_STOCKS, 9, 11,
                          report.stocks_report.plumpy_sup_lost)
    xls_update_value_only(sheet_STOCKS, 11, 11,
                          report.stocks_report.plumpy_sup_balance)
    xls_update_value_only(sheet_STOCKS, 3, 12,
                          report.stocks_report.supercereal_initial)
    xls_update_value_only(sheet_STOCKS, 5, 12,
                          report.stocks_report.supercereal_received)
    xls_update_value_only(sheet_STOCKS, 7, 12,
                          report.stocks_report.supercereal_used)
    xls_update_value_only(sheet_STOCKS, 9, 12,
                          report.stocks_report.supercereal_lost)
    xls_update_value_only(sheet_STOCKS, 11, 12,
                          report.stocks_report.supercereal_balance)
    xls_update_value_only(sheet_STOCKS, 3, 13,
                          report.stocks_report.supercereal_plus_initial)
    xls_update_value_only(sheet_STOCKS, 5, 13,
                          report.stocks_report.supercereal_plus_received)
    xls_update_value_only(sheet_STOCKS, 7, 13,
                          report.stocks_report.supercereal_plus_used)
    xls_update_value_only(sheet_STOCKS, 9, 13,
                          report.stocks_report.supercereal_plus_lost)
    xls_update_value_only(sheet_STOCKS, 11, 13,
                          report.stocks_report.supercereal_plus_balance)
    xls_update_value_only(sheet_STOCKS, 3, 14,
                          report.stocks_report.oil_initial)
    xls_update_value_only(sheet_STOCKS, 5, 14,
                          report.stocks_report.oil_received)
    xls_update_value_only(sheet_STOCKS, 7, 14,
                          report.stocks_report.oil_used)
    xls_update_value_only(sheet_STOCKS, 9, 14,
                          report.stocks_report.oil_lost)
    xls_update_value_only(sheet_STOCKS, 11, 14,
                          report.stocks_report.oil_balance)
    xls_update_value_only(sheet_STOCKS, 3, 15,
                          report.stocks_report.amoxycilline_125_vials_initial)
    xls_update_value_only(sheet_STOCKS, 5, 15,
                          report.stocks_report.amoxycilline_125_vials_received)
    xls_update_value_only(sheet_STOCKS, 7, 15,
                          report.stocks_report.amoxycilline_125_vials_used)
    xls_update_value_only(sheet_STOCKS, 9, 15,
                          report.stocks_report.amoxycilline_125_vials_lost)
    xls_update_value_only(sheet_STOCKS, 11, 15,
                          report.stocks_report.amoxycilline_125_vials_balance)
    xls_update_value_only(sheet_STOCKS, 3, 16,
                          report.stocks_report.amoxycilline_250_caps_initial)
    xls_update_value_only(sheet_STOCKS, 5, 16,
                          report.stocks_report.amoxycilline_250_caps_received)
    xls_update_value_only(sheet_STOCKS, 7, 16,
                          report.stocks_report.amoxycilline_250_caps_used)
    xls_update_value_only(sheet_STOCKS, 9, 16,
                          report.stocks_report.amoxycilline_250_caps_lost)
    xls_update_value_only(sheet_STOCKS, 11, 16,
                          report.stocks_report.amoxycilline_250_caps_balance)
    xls_update_value_only(sheet_STOCKS, 3, 17,
                          report.stocks_report.albendazole_400_initial)
    xls_update_value_only(sheet_STOCKS, 5, 17,
                          report.stocks_report.albendazole_400_received)
    xls_update_value_only(sheet_STOCKS, 7, 17,
                          report.stocks_report.albendazole_400_used)
    xls_update_value_only(sheet_STOCKS, 9, 17,
                          report.stocks_report.albendazole_400_lost)
    xls_update_value_only(sheet_STOCKS, 11, 17,
                          report.stocks_report.albendazole_400_balance)
    xls_update_value_only(sheet_STOCKS, 3, 18,
                          report.stocks_report.vita_100_injectable_initial)
    xls_update_value_only(sheet_STOCKS, 5, 18,
                          report.stocks_report.vita_100_injectable_received)
    xls_update_value_only(sheet_STOCKS, 7, 18,
                          report.stocks_report.vita_100_injectable_used)
    xls_update_value_only(sheet_STOCKS, 9, 18,
                          report.stocks_report.vita_100_injectable_lost)
    xls_update_value_only(sheet_STOCKS, 11, 18,
                          report.stocks_report.vita_100_injectable_balance)
    xls_update_value_only(sheet_STOCKS, 3, 19,
                          report.stocks_report.vita_200_injectable_initial)
    xls_update_value_only(sheet_STOCKS, 5, 19,
                          report.stocks_report.vita_200_injectable_received)
    xls_update_value_only(sheet_STOCKS, 7, 19,
                          report.stocks_report.vita_200_injectable_used)
    xls_update_value_only(sheet_STOCKS, 9, 19,
                          report.stocks_report.vita_200_injectable_lost)
    xls_update_value_only(sheet_STOCKS, 11, 19,
                          report.stocks_report.vita_200_injectable_balance)
    xls_update_value_only(sheet_STOCKS, 3, 20,
                          report.stocks_report.iron_folic_acid_initial)
    xls_update_value_only(sheet_STOCKS, 5, 20,
                          report.stocks_report.iron_folic_acid_received)
    xls_update_value_only(sheet_STOCKS, 7, 20,
                          report.stocks_report.iron_folic_acid_used)
    xls_update_value_only(sheet_STOCKS, 9, 20,
                          report.stocks_report.iron_folic_acid_lost)
    xls_update_value_only(sheet_STOCKS, 11, 20,
                          report.stocks_report.iron_folic_acid_balance)

    # URENAM
    if report.urenam_report:
        xls_update_value_only(sheet_URENAMURENAS, 1, 14,
                              report.urenam_report.u23o6_total_start)
        xls_update_value_only(sheet_URENAMURENAS, 2, 14,
                              report.urenam_report.u23o6_total_start_m)
        xls_update_value_only(sheet_URENAMURENAS, 3, 14,
                              report.urenam_report.u23o6_total_start_f)
        xls_update_value_only(sheet_URENAMURENAS, 4, 14,
                              report.urenam_report.u23o6_new_cases)
        xls_update_value_only(sheet_URENAMURENAS, 7, 14,
                              report.urenam_report.u23o6_returned)
        xls_update_value_only(sheet_URENAMURENAS, 10, 14,
                              report.urenam_report.u23o6_total_in)
        xls_update_value_only(sheet_URENAMURENAS, 11, 14,
                              report.urenam_report.u23o6_total_in_m)
        xls_update_value_only(sheet_URENAMURENAS, 12, 14,
                              report.urenam_report.u23o6_total_in_f)
        xls_update_value_only(sheet_URENAMURENAS, 14, 14,
                              report.urenam_report.u23o6_grand_total_in)
        xls_update_value_only(sheet_URENAMURENAS, 1, 29,
                              report.urenam_report.u23o6_healed)
        xls_update_value_only(sheet_URENAMURENAS, 3, 29,
                              report.urenam_report.u23o6_deceased)
        xls_update_value_only(sheet_URENAMURENAS, 5, 29,
                              report.urenam_report.u23o6_abandon)
        xls_update_value_only(sheet_URENAMURENAS, 7, 29,
                              report.urenam_report.u23o6_not_responding)
        xls_update_value_only(sheet_URENAMURENAS, 8, 29,
                              report.urenam_report.u23o6_total_out)
        xls_update_value_only(sheet_URENAMURENAS, 10, 29,
                              report.urenam_report.u23o6_total_out_m)
        xls_update_value_only(sheet_URENAMURENAS, 11, 29,
                              report.urenam_report.u23o6_total_out_f)
        xls_update_value_only(sheet_URENAMURENAS, 12, 29,
                              report.urenam_report.u23o6_referred)
        xls_update_value_only(sheet_URENAMURENAS, 14, 29,
                              report.urenam_report.u23o6_grand_total_out)
        xls_update_value_only(sheet_URENAMURENAS, 15, 29,
                              report.urenam_report.u23o6_total_end)
        xls_update_value_only(sheet_URENAMURENAS, 14, 29,
                              report.urenam_report.u23o6_grand_total_out)
        xls_update_value_only(sheet_URENAMURENAS, 16, 29,
                              report.urenam_report.u23o6_total_end_m)
        xls_update_value_only(sheet_URENAMURENAS, 14, 29,
                              report.urenam_report.u23o6_grand_total_out)
        xls_update_value_only(sheet_URENAMURENAS, 17, 29,
                              report.urenam_report.u23o6_total_end_f)
        xls_update_value_only(sheet_URENAMURENAS, 1, 15,
                              report.urenam_report.u59o23_total_start)
        xls_update_value_only(sheet_URENAMURENAS, 2, 15,
                              report.urenam_report.u59o23_total_start_m)
        xls_update_value_only(sheet_URENAMURENAS, 3, 15,
                              report.urenam_report.u59o23_total_start_f)
        xls_update_value_only(sheet_URENAMURENAS, 4, 15,
                              report.urenam_report.u59o23_new_cases)
        xls_update_value_only(sheet_URENAMURENAS, 7, 15,
                              report.urenam_report.u59o23_returned)
        xls_update_value_only(sheet_URENAMURENAS, 10, 15,
                              report.urenam_report.u59o23_total_in)
        xls_update_value_only(sheet_URENAMURENAS, 11, 15,
                              report.urenam_report.u59o23_total_in_m)
        xls_update_value_only(sheet_URENAMURENAS, 12, 15,
                              report.urenam_report.u59o23_total_in_f)
        xls_update_value_only(sheet_URENAMURENAS, 14, 15,
                              report.urenam_report.u59o23_grand_total_in)
        xls_update_value_only(sheet_URENAMURENAS, 1, 30,
                              report.urenam_report.u59o23_healed)
        xls_update_value_only(sheet_URENAMURENAS, 3, 30,
                              report.urenam_report.u59o23_deceased)
        xls_update_value_only(sheet_URENAMURENAS, 5, 30,
                              report.urenam_report.u59o23_abandon)
        xls_update_value_only(sheet_URENAMURENAS, 7, 30,
                              report.urenam_report.u59o23_not_responding)
        xls_update_value_only(sheet_URENAMURENAS, 8, 30,
                              report.urenam_report.u59o23_total_out)
        xls_update_value_only(sheet_URENAMURENAS, 10, 30,
                              report.urenam_report.u59o23_total_out_m)
        xls_update_value_only(sheet_URENAMURENAS, 11, 30,
                              report.urenam_report.u59o23_total_out_f)
        xls_update_value_only(sheet_URENAMURENAS, 12, 30,
                              report.urenam_report.u59o23_referred)
        xls_update_value_only(sheet_URENAMURENAS, 14, 30,
                              report.urenam_report.u59o23_grand_total_out)
        xls_update_value_only(sheet_URENAMURENAS, 15, 30,
                              report.urenam_report.u59o23_total_end)
        xls_update_value_only(sheet_URENAMURENAS, 14, 30,
                              report.urenam_report.u59o23_grand_total_out)
        xls_update_value_only(sheet_URENAMURENAS, 16, 30,
                              report.urenam_report.u59o23_total_end_m)
        xls_update_value_only(sheet_URENAMURENAS, 14, 30,
                              report.urenam_report.u59o23_grand_total_out)
        xls_update_value_only(sheet_URENAMURENAS, 17, 30,
                              report.urenam_report.u59o23_total_end_f)
        xls_update_value_only(sheet_URENAMURENAS, 1, 16,
                              report.urenam_report.o59_total_start)
        xls_update_value_only(sheet_URENAMURENAS, 2, 16,
                              report.urenam_report.o59_total_start_m)
        xls_update_value_only(sheet_URENAMURENAS, 3, 16,
                              report.urenam_report.o59_total_start_f)
        xls_update_value_only(sheet_URENAMURENAS, 4, 16,
                              report.urenam_report.o59_new_cases)
        xls_update_value_only(sheet_URENAMURENAS, 7, 16,
                              report.urenam_report.o59_returned)
        xls_update_value_only(sheet_URENAMURENAS, 10, 16,
                              report.urenam_report.o59_total_in)
        xls_update_value_only(sheet_URENAMURENAS, 11, 16,
                              report.urenam_report.o59_total_in_m)
        xls_update_value_only(sheet_URENAMURENAS, 12, 16,
                              report.urenam_report.o59_total_in_f)
        xls_update_value_only(sheet_URENAMURENAS, 14, 16,
                              report.urenam_report.o59_grand_total_in)
        xls_update_value_only(sheet_URENAMURENAS, 1, 31,
                              report.urenam_report.o59_healed)
        xls_update_value_only(sheet_URENAMURENAS, 3, 31,
                              report.urenam_report.o59_deceased)
        xls_update_value_only(sheet_URENAMURENAS, 5, 31,
                              report.urenam_report.o59_abandon)
        xls_update_value_only(sheet_URENAMURENAS, 7, 31,
                              report.urenam_report.o59_not_responding)
        xls_update_value_only(sheet_URENAMURENAS, 8, 31,
                              report.urenam_report.o59_total_out)
        xls_update_value_only(sheet_URENAMURENAS, 10, 31,
                              report.urenam_report.o59_total_out_m)
        xls_update_value_only(sheet_URENAMURENAS, 11, 31,
                              report.urenam_report.o59_total_out_f)
        xls_update_value_only(sheet_URENAMURENAS, 12, 31,
                              report.urenam_report.o59_referred)
        xls_update_value_only(sheet_URENAMURENAS, 14, 31,
                              report.urenam_report.o59_grand_total_out)
        xls_update_value_only(sheet_URENAMURENAS, 15, 31,
                              report.urenam_report.o59_total_end)
        xls_update_value_only(sheet_URENAMURENAS, 14, 31,
                              report.urenam_report.o59_grand_total_out)
        xls_update_value_only(sheet_URENAMURENAS, 16, 31,
                              report.urenam_report.o59_total_end_m)
        xls_update_value_only(sheet_URENAMURENAS, 14, 31,
                              report.urenam_report.o59_grand_total_out)
        xls_update_value_only(sheet_URENAMURENAS, 17, 31,
                              report.urenam_report.o59_total_end_f)
        xls_update_value_only(sheet_URENAMURENAS, 1, 17,
                              report.urenam_report.pw_total_start)
        xls_update_value_only(sheet_URENAMURENAS, 3, 17,
                              report.urenam_report.pw_total_start_f)
        xls_update_value_only(sheet_URENAMURENAS, 4, 17,
                              report.urenam_report.pw_new_cases)
        xls_update_value_only(sheet_URENAMURENAS, 7, 17,
                              report.urenam_report.pw_returned)
        xls_update_value_only(sheet_URENAMURENAS, 10, 17,
                              report.urenam_report.pw_total_in)
        xls_update_value_only(sheet_URENAMURENAS, 12, 17,
                              report.urenam_report.pw_total_in_f)
        xls_update_value_only(sheet_URENAMURENAS, 14, 17,
                              report.urenam_report.pw_grand_total_in)
        xls_update_value_only(sheet_URENAMURENAS, 1, 32,
                              report.urenam_report.pw_healed)
        xls_update_value_only(sheet_URENAMURENAS, 3, 32,
                              report.urenam_report.pw_deceased)
        xls_update_value_only(sheet_URENAMURENAS, 5, 32,
                              report.urenam_report.pw_abandon)
        xls_update_value_only(sheet_URENAMURENAS, 7, 32,
                              report.urenam_report.pw_not_responding)
        xls_update_value_only(sheet_URENAMURENAS, 8, 32,
                              report.urenam_report.pw_total_out)
        xls_update_value_only(sheet_URENAMURENAS, 11, 32,
                              report.urenam_report.pw_total_out_f)
        xls_update_value_only(sheet_URENAMURENAS, 12, 32,
                              report.urenam_report.pw_referred)
        xls_update_value_only(sheet_URENAMURENAS, 14, 32,
                              report.urenam_report.pw_grand_total_out)
        xls_update_value_only(sheet_URENAMURENAS, 15, 32,
                              report.urenam_report.pw_total_end)
        xls_update_value_only(sheet_URENAMURENAS, 14, 32,
                              report.urenam_report.pw_grand_total_out)
        xls_update_value_only(sheet_URENAMURENAS, 17, 32,
                              report.urenam_report.pw_total_end_f)
        xls_update_value_only(sheet_URENAMURENAS, 1, 18,
                              report.urenam_report.exsam_total_start)
        xls_update_value_only(sheet_URENAMURENAS, 2, 18,
                              report.urenam_report.exsam_total_start_m)
        xls_update_value_only(sheet_URENAMURENAS, 3, 18,
                              report.urenam_report.exsam_total_start_f)
        xls_update_value_only(sheet_URENAMURENAS, 14, 18,
                              report.urenam_report.exsam_grand_total_in)
        xls_update_value_only(sheet_URENAMURENAS, 12, 33,
                              report.urenam_report.exsam_referred)
        xls_update_value_only(sheet_URENAMURENAS, 14, 33,
                              report.urenam_report.exsam_grand_total_out)
        xls_update_value_only(sheet_URENAMURENAS, 15, 33,
                              report.urenam_report.exsam_total_end)
        xls_update_value_only(sheet_URENAMURENAS, 14, 33,
                              report.urenam_report.exsam_grand_total_out)
        xls_update_value_only(sheet_URENAMURENAS, 16, 33,
                              report.urenam_report.exsam_total_end_m)
        xls_update_value_only(sheet_URENAMURENAS, 14, 33,
                              report.urenam_report.exsam_grand_total_out)
        xls_update_value_only(sheet_URENAMURENAS, 17, 33,
                              report.urenam_report.exsam_total_end_f)
        #####
        xls_update_value_only(sheet_URENAMURENAS, 1, 19,
                              report.urenam_report.total_start)
        xls_update_value_only(sheet_URENAMURENAS, 2, 19,
                              report.urenam_report.total_start_m)
        xls_update_value_only(sheet_URENAMURENAS, 3, 19,
                              report.urenam_report.total_start_f)
        xls_update_value_only(sheet_URENAMURENAS, 4, 19,
                              report.urenam_report.new_cases)
        xls_update_value_only(sheet_URENAMURENAS, 7, 19,
                              report.urenam_report.returned)
        xls_update_value_only(sheet_URENAMURENAS, 10, 19,
                              report.urenam_report.total_in)
        xls_update_value_only(sheet_URENAMURENAS, 11, 19,
                              report.urenam_report.total_in_m)
        xls_update_value_only(sheet_URENAMURENAS, 12, 19,
                              report.urenam_report.total_in_f)
        xls_update_value_only(sheet_URENAMURENAS, 14, 19,
                              report.urenam_report.grand_total_in)
        xls_update_value_only(sheet_URENAMURENAS, 1, 34,
                              report.urenam_report.healed)
        xls_update_value_only(sheet_URENAMURENAS, 3, 34,
                              report.urenam_report.deceased)
        xls_update_value_only(sheet_URENAMURENAS, 5, 34,
                              report.urenam_report.abandon)
        xls_update_value_only(sheet_URENAMURENAS, 7, 34,
                              report.urenam_report.not_responding)
        xls_update_value_only(sheet_URENAMURENAS, 8, 34,
                              report.urenam_report.total_out)
        xls_update_value_only(sheet_URENAMURENAS, 10, 34,
                              report.urenam_report.total_out_m)
        xls_update_value_only(sheet_URENAMURENAS, 11, 34,
                              report.urenam_report.total_out_f)
        xls_update_value_only(sheet_URENAMURENAS, 12, 34,
                              report.urenam_report.referred)
        xls_update_value_only(sheet_URENAMURENAS, 14, 34,
                              report.urenam_report.grand_total_out)
        xls_update_value_only(sheet_URENAMURENAS, 15, 34,
                              report.urenam_report.total_end)
        xls_update_value_only(sheet_URENAMURENAS, 14, 34,
                              report.urenam_report.grand_total_out)
        xls_update_value_only(sheet_URENAMURENAS, 16, 34,
                              report.urenam_report.total_end_m)
        xls_update_value_only(sheet_URENAMURENAS, 14, 34,
                              report.urenam_report.grand_total_out)
        xls_update_value_only(sheet_URENAMURENAS, 17, 34,
                              report.urenam_report.total_end_f)

    # URENAS
    if report.urenas_report:
        xls_update_value_only(sheet_URENAMURENAS, 1, 10,
                              report.urenas_report.u59o6_total_start)
        xls_update_value_only(sheet_URENAMURENAS, 2, 10,
                              report.urenas_report.u59o6_total_start_m)
        xls_update_value_only(sheet_URENAMURENAS, 3, 10,
                              report.urenas_report.u59o6_total_start_f)
        xls_update_value_only(sheet_URENAMURENAS, 4, 10,
                              report.urenas_report.u59o6_new_cases)
        xls_update_value_only(sheet_URENAMURENAS, 7, 10,
                              report.urenas_report.u59o6_returned)
        xls_update_value_only(sheet_URENAMURENAS, 10, 10,
                              report.urenas_report.u59o6_total_in)
        xls_update_value_only(sheet_URENAMURENAS, 11, 10,
                              report.urenas_report.u59o6_total_in_m)
        xls_update_value_only(sheet_URENAMURENAS, 12, 10,
                              report.urenas_report.u59o6_total_in_f)
        xls_update_value_only(sheet_URENAMURENAS, 13, 10,
                              report.urenas_report.u59o6_transferred)
        xls_update_value_only(sheet_URENAMURENAS, 14, 10,
                              report.urenas_report.u59o6_grand_total_in)
        xls_update_value_only(sheet_URENAMURENAS, 1, 25,
                              report.urenas_report.u59o6_healed)
        xls_update_value_only(sheet_URENAMURENAS, 3, 25,
                              report.urenas_report.u59o6_deceased)
        xls_update_value_only(sheet_URENAMURENAS, 5, 25,
                              report.urenas_report.u59o6_abandon)
        xls_update_value_only(sheet_URENAMURENAS, 7, 25,
                              report.urenas_report.u59o6_not_responding)
        xls_update_value_only(sheet_URENAMURENAS, 8, 25,
                              report.urenas_report.u59o6_total_out)
        xls_update_value_only(sheet_URENAMURENAS, 10, 25,
                              report.urenas_report.u59o6_total_out_m)
        xls_update_value_only(sheet_URENAMURENAS, 11, 25,
                              report.urenas_report.u59o6_total_out_f)
        xls_update_value_only(sheet_URENAMURENAS, 12, 25,
                              report.urenas_report.u59o6_referred)
        xls_update_value_only(sheet_URENAMURENAS, 14, 25,
                              report.urenas_report.u59o6_grand_total_out)
        xls_update_value_only(sheet_URENAMURENAS, 15, 25,
                              report.urenas_report.u59o6_total_end)
        xls_update_value_only(sheet_URENAMURENAS, 14, 25,
                              report.urenas_report.u59o6_grand_total_out)
        xls_update_value_only(sheet_URENAMURENAS, 16, 25,
                              report.urenas_report.u59o6_total_end_m)
        xls_update_value_only(sheet_URENAMURENAS, 14, 25,
                              report.urenas_report.u59o6_grand_total_out)
        xls_update_value_only(sheet_URENAMURENAS, 17, 25,
                              report.urenas_report.u59o6_total_end_f)
        xls_update_value_only(sheet_URENAMURENAS, 1, 11,
                              report.urenas_report.o59_total_start)
        xls_update_value_only(sheet_URENAMURENAS, 2, 11,
                              report.urenas_report.o59_total_start_m)
        xls_update_value_only(sheet_URENAMURENAS, 3, 11,
                              report.urenas_report.o59_total_start_f)
        xls_update_value_only(sheet_URENAMURENAS, 4, 11,
                              report.urenas_report.o59_new_cases)
        xls_update_value_only(sheet_URENAMURENAS, 7, 11,
                              report.urenas_report.o59_returned)
        xls_update_value_only(sheet_URENAMURENAS, 10, 11,
                              report.urenas_report.o59_total_in)
        xls_update_value_only(sheet_URENAMURENAS, 11, 11,
                              report.urenas_report.o59_total_in_m)
        xls_update_value_only(sheet_URENAMURENAS, 12, 11,
                              report.urenas_report.o59_total_in_f)
        xls_update_value_only(sheet_URENAMURENAS, 13, 11,
                              report.urenas_report.o59_transferred)
        xls_update_value_only(sheet_URENAMURENAS, 14, 11,
                              report.urenas_report.o59_grand_total_in)
        xls_update_value_only(sheet_URENAMURENAS, 1, 26,
                              report.urenas_report.o59_healed)
        xls_update_value_only(sheet_URENAMURENAS, 3, 26,
                              report.urenas_report.o59_deceased)
        xls_update_value_only(sheet_URENAMURENAS, 5, 26,
                              report.urenas_report.o59_abandon)
        xls_update_value_only(sheet_URENAMURENAS, 7, 26,
                              report.urenas_report.o59_not_responding)
        xls_update_value_only(sheet_URENAMURENAS, 8, 26,
                              report.urenas_report.o59_total_out)
        xls_update_value_only(sheet_URENAMURENAS, 10, 26,
                              report.urenas_report.o59_total_out_m)
        xls_update_value_only(sheet_URENAMURENAS, 11, 26,
                              report.urenas_report.o59_total_out_f)
        xls_update_value_only(sheet_URENAMURENAS, 12, 26,
                              report.urenas_report.o59_referred)
        xls_update_value_only(sheet_URENAMURENAS, 14, 26,
                              report.urenas_report.o59_grand_total_out)
        xls_update_value_only(sheet_URENAMURENAS, 15, 26,
                              report.urenas_report.o59_total_end)
        xls_update_value_only(sheet_URENAMURENAS, 14, 26,
                              report.urenas_report.o59_grand_total_out)
        xls_update_value_only(sheet_URENAMURENAS, 16, 26,
                              report.urenas_report.o59_total_end_m)
        xls_update_value_only(sheet_URENAMURENAS, 14, 26,
                              report.urenas_report.o59_grand_total_out)
        xls_update_value_only(sheet_URENAMURENAS, 17, 26,
                              report.urenas_report.o59_total_end_f)
        xls_update_value_only(sheet_URENAMURENAS, 1, 12,
                              report.urenas_report.total_start)
        xls_update_value_only(sheet_URENAMURENAS, 2, 12,
                              report.urenas_report.total_start_m)
        xls_update_value_only(sheet_URENAMURENAS, 3, 12,
                              report.urenas_report.total_start_f)
        xls_update_value_only(sheet_URENAMURENAS, 4, 12,
                              report.urenas_report.new_cases)
        xls_update_value_only(sheet_URENAMURENAS, 7, 12,
                              report.urenas_report.returned)
        xls_update_value_only(sheet_URENAMURENAS, 10, 12,
                              report.urenas_report.total_in)
        xls_update_value_only(sheet_URENAMURENAS, 11, 12,
                              report.urenas_report.total_in_m)
        xls_update_value_only(sheet_URENAMURENAS, 12, 12,
                              report.urenas_report.total_in_f)
        xls_update_value_only(sheet_URENAMURENAS, 14, 12,
                              report.urenas_report.grand_total_in)
        xls_update_value_only(sheet_URENAMURENAS, 1, 27,
                              report.urenas_report.healed)
        xls_update_value_only(sheet_URENAMURENAS, 3, 27,
                              report.urenas_report.deceased)
        xls_update_value_only(sheet_URENAMURENAS, 5, 27,
                              report.urenas_report.abandon)
        xls_update_value_only(sheet_URENAMURENAS, 7, 27,
                              report.urenas_report.not_responding)
        xls_update_value_only(sheet_URENAMURENAS, 8, 27,
                              report.urenas_report.total_out)
        xls_update_value_only(sheet_URENAMURENAS, 10, 27,
                              report.urenas_report.total_out_m)
        xls_update_value_only(sheet_URENAMURENAS, 11, 27,
                              report.urenas_report.total_out_f)
        xls_update_value_only(sheet_URENAMURENAS, 12, 27,
                              report.urenas_report.referred)
        xls_update_value_only(sheet_URENAMURENAS, 14, 27,
                              report.urenas_report.grand_total_out)
        xls_update_value_only(sheet_URENAMURENAS, 15, 27,
                              report.urenas_report.total_end)
        xls_update_value_only(sheet_URENAMURENAS, 14, 27,
                              report.urenas_report.grand_total_out)
        xls_update_value_only(sheet_URENAMURENAS, 16, 27,
                              report.urenas_report.total_end_m)
        xls_update_value_only(sheet_URENAMURENAS, 14, 27,
                              report.urenas_report.grand_total_out)
        xls_update_value_only(sheet_URENAMURENAS, 17, 27,
                              report.urenas_report.total_end_f)

    # URENI
    if report.ureni_report:
        xls_update_value_only(sheet_URENI, 1, 10,
                              report.ureni_report.u6_total_start)
        xls_update_value_only(sheet_URENI, 2, 10,
                              report.ureni_report.u6_total_start_m)
        xls_update_value_only(sheet_URENI, 3, 10,
                              report.ureni_report.u6_total_start_f)
        xls_update_value_only(sheet_URENI, 4, 10,
                              report.ureni_report.u6_new_cases)
        xls_update_value_only(sheet_URENI, 7, 10,
                              report.ureni_report.u6_returned)
        xls_update_value_only(sheet_URENI, 10, 10,
                              report.ureni_report.u6_total_in)
        xls_update_value_only(sheet_URENI, 11, 10,
                              report.ureni_report.u6_total_in_m)
        xls_update_value_only(sheet_URENI, 12, 10,
                              report.ureni_report.u6_total_in_f)
        xls_update_value_only(sheet_URENI, 13, 10,
                              report.ureni_report.u6_transferred)
        xls_update_value_only(sheet_URENI, 14, 10,
                              report.ureni_report.u6_grand_total_in)
        xls_update_value_only(sheet_URENI, 1, 19,
                              report.ureni_report.u6_healed)
        xls_update_value_only(sheet_URENI, 3, 19,
                              report.ureni_report.u6_deceased)
        xls_update_value_only(sheet_URENI, 5, 19,
                              report.ureni_report.u6_abandon)
        xls_update_value_only(sheet_URENI, 7, 19,
                              report.ureni_report.u6_not_responding)
        xls_update_value_only(sheet_URENI, 8, 19,
                              report.ureni_report.u6_total_out)
        xls_update_value_only(sheet_URENI, 10, 19,
                              report.ureni_report.u6_total_out_m)
        xls_update_value_only(sheet_URENI, 11, 19,
                              report.ureni_report.u6_total_out_f)
        xls_update_value_only(sheet_URENI, 12, 19,
                              report.ureni_report.u6_referred)
        xls_update_value_only(sheet_URENI, 14, 19,
                              report.ureni_report.u6_grand_total_out)
        xls_update_value_only(sheet_URENI, 15, 19,
                              report.ureni_report.u6_total_end)
        xls_update_value_only(sheet_URENI, 14, 19,
                              report.ureni_report.u6_grand_total_out)
        xls_update_value_only(sheet_URENI, 16, 19,
                              report.ureni_report.u6_total_end_m)
        xls_update_value_only(sheet_URENI, 14, 19,
                              report.ureni_report.u6_grand_total_out)
        xls_update_value_only(sheet_URENI, 17, 19,
                              report.ureni_report.u6_total_end_f)
        xls_update_value_only(sheet_URENI, 1, 11,
                              report.ureni_report.u59o6_total_start)
        xls_update_value_only(sheet_URENI, 2, 11,
                              report.ureni_report.u59o6_total_start_m)
        xls_update_value_only(sheet_URENI, 3, 11,
                              report.ureni_report.u59o6_total_start_f)
        xls_update_value_only(sheet_URENI, 4, 11,
                              report.ureni_report.u59o6_new_cases)
        xls_update_value_only(sheet_URENI, 7, 11,
                              report.ureni_report.u59o6_returned)
        xls_update_value_only(sheet_URENI, 10, 11,
                              report.ureni_report.u59o6_total_in)
        xls_update_value_only(sheet_URENI, 11, 11,
                              report.ureni_report.u59o6_total_in_m)
        xls_update_value_only(sheet_URENI, 12, 11,
                              report.ureni_report.u59o6_total_in_f)
        xls_update_value_only(sheet_URENI, 13, 11,
                              report.ureni_report.u59o6_transferred)
        xls_update_value_only(sheet_URENI, 14, 11,
                              report.ureni_report.u59o6_grand_total_in)
        xls_update_value_only(sheet_URENI, 1, 20,
                              report.ureni_report.u59o6_healed)
        xls_update_value_only(sheet_URENI, 3, 20,
                              report.ureni_report.u59o6_deceased)
        xls_update_value_only(sheet_URENI, 5, 20,
                              report.ureni_report.u59o6_abandon)
        xls_update_value_only(sheet_URENI, 7, 20,
                              report.ureni_report.u59o6_not_responding)
        xls_update_value_only(sheet_URENI, 8, 20,
                              report.ureni_report.u59o6_total_out)
        xls_update_value_only(sheet_URENI, 10, 20,
                              report.ureni_report.u59o6_total_out_m)
        xls_update_value_only(sheet_URENI, 11, 20,
                              report.ureni_report.u59o6_total_out_f)
        xls_update_value_only(sheet_URENI, 12, 20,
                              report.ureni_report.u59o6_referred)
        xls_update_value_only(sheet_URENI, 14, 20,
                              report.ureni_report.u59o6_grand_total_out)
        xls_update_value_only(sheet_URENI, 15, 20,
                              report.ureni_report.u59o6_total_end)
        xls_update_value_only(sheet_URENI, 14, 20,
                              report.ureni_report.u59o6_grand_total_out)
        xls_update_value_only(sheet_URENI, 16, 20,
                              report.ureni_report.u59o6_total_end_m)
        xls_update_value_only(sheet_URENI, 14, 20,
                              report.ureni_report.u59o6_grand_total_out)
        xls_update_value_only(sheet_URENI, 17, 20,
                              report.ureni_report.u59o6_total_end_f)
        xls_update_value_only(sheet_URENI, 1, 12,
                              report.ureni_report.o59_total_start)
        xls_update_value_only(sheet_URENI, 2, 12,
                              report.ureni_report.o59_total_start_m)
        xls_update_value_only(sheet_URENI, 3, 12,
                              report.ureni_report.o59_total_start_f)
        xls_update_value_only(sheet_URENI, 4, 12,
                              report.ureni_report.o59_new_cases)
        xls_update_value_only(sheet_URENI, 7, 12,
                              report.ureni_report.o59_returned)
        xls_update_value_only(sheet_URENI, 10, 12,
                              report.ureni_report.o59_total_in)
        xls_update_value_only(sheet_URENI, 11, 12,
                              report.ureni_report.o59_total_in_m)
        xls_update_value_only(sheet_URENI, 12, 12,
                              report.ureni_report.o59_total_in_f)
        xls_update_value_only(sheet_URENI, 13, 12,
                              report.ureni_report.o59_transferred)
        xls_update_value_only(sheet_URENI, 14, 12,
                              report.ureni_report.o59_grand_total_in)
        xls_update_value_only(sheet_URENI, 1, 21,
                              report.ureni_report.o59_healed)
        xls_update_value_only(sheet_URENI, 3, 21,
                              report.ureni_report.o59_deceased)
        xls_update_value_only(sheet_URENI, 5, 21,
                              report.ureni_report.o59_abandon)
        xls_update_value_only(sheet_URENI, 7, 21,
                              report.ureni_report.o59_not_responding)
        xls_update_value_only(sheet_URENI, 8, 21,
                              report.ureni_report.o59_total_out)
        xls_update_value_only(sheet_URENI, 10, 21,
                              report.ureni_report.o59_total_out_m)
        xls_update_value_only(sheet_URENI, 11, 21,
                              report.ureni_report.o59_total_out_f)
        xls_update_value_only(sheet_URENI, 12, 21,
                              report.ureni_report.o59_referred)
        xls_update_value_only(sheet_URENI, 14, 21,
                              report.ureni_report.o59_grand_total_out)
        xls_update_value_only(sheet_URENI, 15, 21,
                              report.ureni_report.o59_total_end)
        xls_update_value_only(sheet_URENI, 14, 21,
                              report.ureni_report.o59_grand_total_out)
        xls_update_value_only(sheet_URENI, 16, 21,
                              report.ureni_report.o59_total_end_m)
        xls_update_value_only(sheet_URENI, 14, 21,
                              report.ureni_report.o59_grand_total_out)
        xls_update_value_only(sheet_URENI, 17, 21,
                              report.ureni_report.o59_total_end_f)
        xls_update_value_only(sheet_URENI, 1, 13,
                              report.ureni_report.total_start)
        xls_update_value_only(sheet_URENI, 2, 13,
                              report.ureni_report.total_start_m)
        xls_update_value_only(sheet_URENI, 3, 13,
                              report.ureni_report.total_start_f)
        xls_update_value_only(sheet_URENI, 4, 13,
                              report.ureni_report.new_cases)
        xls_update_value_only(sheet_URENI, 7, 13,
                              report.ureni_report.returned)
        xls_update_value_only(sheet_URENI, 10, 13,
                              report.ureni_report.total_in)
        xls_update_value_only(sheet_URENI, 11, 13,
                              report.ureni_report.total_in_m)
        xls_update_value_only(sheet_URENI, 12, 13,
                              report.ureni_report.total_in_f)
        xls_update_value_only(sheet_URENI, 14, 13,
                              report.ureni_report.grand_total_in)
        xls_update_value_only(sheet_URENI, 1, 22,
                              report.ureni_report.healed)
        xls_update_value_only(sheet_URENI, 3, 22,
                              report.ureni_report.deceased)
        xls_update_value_only(sheet_URENI, 5, 22,
                              report.ureni_report.abandon)
        xls_update_value_only(sheet_URENI, 7, 22,
                              report.ureni_report.not_responding)
        xls_update_value_only(sheet_URENI, 8, 22,
                              report.ureni_report.total_out)
        xls_update_value_only(sheet_URENI, 10, 22,
                              report.ureni_report.total_out_m)
        xls_update_value_only(sheet_URENI, 11, 22,
                              report.ureni_report.total_out_f)
        xls_update_value_only(sheet_URENI, 12, 22,
                              report.ureni_report.referred)
        xls_update_value_only(sheet_URENI, 14, 22,
                              report.ureni_report.grand_total_out)
        xls_update_value_only(sheet_URENI, 15, 22,
                              report.ureni_report.total_end)
        xls_update_value_only(sheet_URENI, 14, 22,
                              report.ureni_report.grand_total_out)
        xls_update_value_only(sheet_URENI, 16, 22,
                              report.ureni_report.total_end_m)
        xls_update_value_only(sheet_URENI, 14, 22,
                              report.ureni_report.grand_total_out)
        xls_update_value_only(sheet_URENI, 17, 22,
                              report.ureni_report.total_end_f)

    stream = StringIO.StringIO()
    copy_week_b.save(stream)

    return stream


def nutrition_overview_xls(entity, periods, is_sam=False, is_mam=False):
    """ Exports complete SAM/MAM Overview data as XLS """

    # from snisi_nutrition.utils import generate_sum_data_table_for
    from snisi_nutrition.models.URENAM import URENAMNutritionR
    from snisi_nutrition.models.URENI import URENINutritionR
    from snisi_nutrition.models.URENAS import URENASNutritionR
    from snisi_nutrition.models.Common import AbstractURENutritionR

    from snisi_core.models.Entities import Entity
    from snisi_core.models.Projects import Cluster
    from snisi_core.models.Reporting import ExpectedReporting

    # styles
    border_all_regular = xlwt.Borders()
    border_all_regular.left = 1
    border_all_regular.right = 1
    border_all_regular.top = 1
    border_all_regular.bottom = 1

    border_bottom_large = xlwt.Borders()
    border_bottom_large.left = 0
    border_bottom_large.right = 0
    border_bottom_large.top = 0
    border_bottom_large.bottom = 2

    font_regular = xlwt.Font()
    font_regular.bold = False
    font_regular.height = 12 * 0x14

    font_bold = xlwt.Font()
    font_bold.bold = True
    font_bold.height = 12 * 0x14

    font_title = xlwt.Font()
    font_title.bold = True
    font_title.height = 16 * 0x14

    align_center = xlwt.Alignment()
    align_center.horz = xlwt.Alignment.HORZ_CENTER
    align_center.vert = xlwt.Alignment.VERT_CENTER

    align_left = xlwt.Alignment()
    align_left.horz = xlwt.Alignment.HORZ_LEFT
    align_left.vert = xlwt.Alignment.VERT_CENTER

    color_empty = xlwt.Pattern()
    color_empty.pattern = xlwt.Pattern.SOLID_PATTERN
    color_empty.pattern_fore_colour = 8

    color_lightgrey = xlwt.Pattern()
    color_lightgrey.pattern = xlwt.Pattern.SOLID_PATTERN
    color_lightgrey.pattern_fore_colour = 22

    style_title = xlwt.XFStyle()
    style_title.alignment = align_center
    style_title.borders = border_bottom_large
    style_title.font = font_title

    style_label = xlwt.XFStyle()
    style_label.alignment = align_left
    style_label.borders = border_all_regular
    style_label.font = font_bold

    style_label_sum = copy.deepcopy(style_label)
    style_label_sum.pattern = color_lightgrey

    style_value = xlwt.XFStyle()
    style_value.alignment = align_center
    style_value.borders = border_all_regular
    style_value.font = font_regular

    style_value_pc = xlwt.XFStyle()
    style_value_pc.alignment = align_center
    style_value_pc.borders = border_all_regular
    style_value_pc.font = font_regular
    style_value_pc.num_format_str = '0%'

    style_value_sum = copy.deepcopy(style_value)
    style_value_sum.pattern = color_lightgrey

    # compute all the data. XLS is just a display of this
    cluster = Cluster.get_or_none('nutrition_routine')
    report_classes = cluster.domain \
        .import_from('expected.report_classes_for')(cluster)

    periods_expecteds = [
        (period, ExpectedReporting.objects.filter(
            period=period, entity=entity,
            report_class__in=report_classes).last())
        for period in periods
    ]

    def wdcm(cm):
        return int(0x0d00 / 2.29 * cm)

    def setwidth(sheet, col, cm):
        sheet.col(col).width = wdcm(cm)

    def htcm(cm):
        return int(342 / 0.6 * cm)

    def setheight(sheet, row, cm):
        sheet.row(row).height = htcm(cm)
        sheet.row(row).height_mismatch = True

    # total_table = generate_sum_data_table_for(entity=entity, periods=periods)

    # prefix is used for sheet names
    prefix = {
        'health_district': "DS",
        'health_region': "DRS"
    }.get(entity.type.slug, "")
    if prefix:
        prefix += " "

    # On crée le doc xls
    book = xlwt.Workbook(encoding='utf-8')

    def write_header(sheet, uren):
        """ writes standard header columns to sheet (SAM/MAM are identical) """

        # main title, all width
        sheet.write_merge(0, 0, 0, 27,
                          "RAPPORTS STATISTIQUES MENSUEL - {uren} {periods}"
                          .format(uren=uren, periods=get_periods_str(periods)),
                          style_title)

        # empty line folowing

        # first line of headers (mostly merged)
        sheet.write_merge(2, 3, 3, 5, "TOTAL DÉBUT DU MOIS", style_label)

        sheet.write_merge(2, 2, 6, 12, "ADMISSIONS", style_label)

        sheet.write_merge(2, 2, 13, 21, "SORTIES", style_label)

        sheet.write_merge(2, 3, 22, 24, "TOTAL FIN DU MOIS", style_label)

        sheet.write_merge(2, 3, 25, 27, "INDICATEURS DE PERFORMANCE",
                          style_label)

        # second line of headers
        sheet.write_merge(3, 6, 6, 6, "NOUVEAUX CAS", style_label)

        sheet.write_merge(3, 6, 7, 7, "RE-ADMISSIONS", style_label)

        sheet.write_merge(3, 4, 8, 10, "Total Admissions", style_label)

        sheet.write_merge(3, 6, 11, 11, "Transfert/Réf. de l'URENI/URENAS",
                          style_label)

        sheet.write_merge(3, 6, 12, 12, "TOTAL ADM GENERAL", style_label)

        sheet.write_merge(3, 6, 13, 13, "Guéris", style_label)

        sheet.write_merge(3, 6, 14, 14, "Décès", style_label)

        sheet.write_merge(3, 6, 15, 15, "Abandons", style_label)

        sheet.write_merge(3, 6, 16, 16, "NR", style_label)

        sheet.write_merge(3, 3, 17, 19, "Total Sorties", style_label)

        sheet.write_merge(3, 6, 20, 20, "Réf. Nut", style_label)

        sheet.write_merge(3, 6, 21, 21, "TOTAL SORTIE GNL", style_label)

        # third line of headers
        sheet.write_merge(4, 6, 17, 17, "Total", style_label)
        sheet.write_merge(4, 6, 18, 18, "M", style_label)
        sheet.write_merge(4, 6, 19, 19, "F", style_label)

        sheet.write_merge(4, 6, 22, 22, "Total fin du mois", style_label)

        sheet.write_merge(4, 6, 23, 23, "M", style_label)

        sheet.write_merge(4, 6, 24, 24, "F", style_label)

        sheet.write_merge(4, 6, 25, 25, "% Guéris", style_label)
        sheet.write_merge(4, 6, 26, 26, "% Décès", style_label)
        sheet.write_merge(4, 6, 27, 27, "% Abandon", style_label)

        # fourth line of headers
        sheet.write_merge(5, 6, 1, 1, "NOM DE LA STRUCTURE", style_label)
        sheet.write_merge(5, 6, 2, 2, "Catégorie d'âge", style_label)

        sheet.write_merge(4, 6, 3, 3, "Total", style_label)
        sheet.write_merge(4, 6, 4, 4, "M", style_label)
        sheet.write_merge(4, 6, 5, 5, "F", style_label)

        sheet.write_merge(5, 6, 8, 8, "Total", style_label)
        sheet.write_merge(5, 6, 9, 9, "M", style_label)
        sheet.write_merge(5, 6, 10, 10, "F", style_label)

        # set columns width
        setwidth(sheet, 0, 2.82)
        setwidth(sheet, 1, 9)
        setwidth(sheet, 2, 2.93)
        setwidth(sheet, 3, 2.29)
        setwidth(sheet, 4, 1.9)
        setwidth(sheet, 5, 1.94)
        setwidth(sheet, 6, 2.54)
        setwidth(sheet, 7, 2.65)
        setwidth(sheet, 8, 2.33)
        setwidth(sheet, 9, 1.8)
        setwidth(sheet, 10, 1.94)
        setwidth(sheet, 11, 3.42)
        setwidth(sheet, 12, 3.39)
        setwidth(sheet, 13, 2.26)
        setwidth(sheet, 14, 2.01)
        setwidth(sheet, 15, 2.54)
        setwidth(sheet, 16, 2.12)
        setwidth(sheet, 17, 2.12)
        setwidth(sheet, 18, 2.05)
        setwidth(sheet, 19, 1.98)
        setwidth(sheet, 20, 2.33)
        setwidth(sheet, 21, 3.85)
        setwidth(sheet, 22, 2.43)
        setwidth(sheet, 23, 1.94)
        setwidth(sheet, 24, 1.98)
        setwidth(sheet, 25, 2.54)
        setwidth(sheet, 26, 2.29)
        setwidth(sheet, 27, 2.43)

        # set row height
        setheight(sheet, 0, 0.74)
        setheight(sheet, 1, 0.56)
        setheight(sheet, 2, 0.53)
        setheight(sheet, 3, 0.56)
        setheight(sheet, 4, 1.03)
        setheight(sheet, 5, 0.61)
        setheight(sheet, 6, 1.19)

    def get_children(entity, is_sam, is_ureni=None):
        def hc_filter(hc, is_sam, is_ureni):
            if is_sam:
                return hc.has_ureni if is_ureni else hc.has_urenas
            else:
                return hc.has_urenam
        if entity.type.slug == 'health_district':
            return [e for e in entity.get_health_centers() if hc_filter(e)]
        elif entity.type.slug == 'health_region':
            return entity.get_health_districts()
        elif entity.type.slug == 'country':
            return entity.get_health_regions()

    def nb_lines_for(reportcls, nb_children):
        # each child has a line for each age group
        # plus one line for total
        # then a total for each age group
        # ending with a final total line
        nb_age_groups = len(reportcls.age_groups())
        return (nb_age_groups + 1) * nb_children + nb_age_groups + 1

    def write_line(sheet, child,
                   age_group, report, expected, row, is_sam, is_ureni):

        is_total = not isinstance(child, Entity)

        print("writing line", child, age_group,  "on ", row, " / ", sheet)

        # age group
        if age_group is None:
            age_group_name = "Total"
        else:
            age_group_name = AbstractURENutritionR.AGE_LABELS.get(
                age_group.replace("sam_", ""), age_group)
        sheet.write(row, 2, age_group_name)

        # use for the all-periods total
        if is_total:
            sreport = report
        else:
            # grab report for that location if exist
            try:
                sreport = [r for r in report.direct_sources()
                           if r.entity.slug == child.slug][0]
            except IndexError:
                sreport = None

        # if no report, leave all fields blank and move to next
        if sreport is None:
            return

        print(age_group_name)

        def gd(report, sk, age_group, field, is_sam=False):
            if field == 'total_start':
                print(report, sk, age_group, field)
            sub_report = {
                'i': 'ureni_report',
                'm': 'urenam_report',
                'a': 'urenas_report',
                's': 'stocks_report'
            }.get(sk)
            if age_group is None:
                fname = field
                if is_sam and sub_report is None:
                    fname = "sam_{}".format(field)
            else:
                fname = "{}_{}".format(age_group, field)

            if sub_report is None:
                if isinstance(report, dict):
                    return report.get(fname)
                return getattr(report, fname)

            return getattr(getattr(report, sub_report), fname, "-")

        sk = 'm'
        if is_sam:
            sk = 'i' if is_ureni else 'a'
            if is_total and is_ureni is None:
                sk = None
            if age_group is None:
                age_group

        # Total debut de mois
        ism = is_sam
        sheet.write(row, 3, gd(sreport, sk,
                    age_group, 'total_start', ism), style_value)
        sheet.write(row, 4, gd(sreport, sk,
                    age_group, 'total_start_m', ism), style_value)
        sheet.write(row, 5, gd(sreport, sk,
                    age_group, 'total_start_f', ism), style_value)
        sheet.write(row, 6, gd(sreport, sk,
                    age_group, 'new_cases', ism), style_value)
        sheet.write(row, 7, gd(sreport, sk,
                    age_group, 'returned', ism), style_value)
        sheet.write(row, 8, gd(sreport, sk,
                    age_group, 'total_in', ism), style_value)
        sheet.write(row, 9, gd(sreport, sk,
                    age_group, 'total_in_m', ism), style_value)
        sheet.write(row, 10, gd(sreport, sk,
                    age_group, 'total_in_f', ism), style_value)
        sheet.write(row, 11, gd(sreport, sk,
                    age_group, 'transferred', ism), style_value)
        sheet.write(row, 12, gd(sreport, sk,
                    age_group, 'grand_total_in', ism), style_value)
        sheet.write(row, 13, gd(sreport, sk,
                    age_group, 'healed', ism), style_value)
        sheet.write(row, 14, gd(sreport, sk,
                    age_group, 'deceased', ism), style_value)
        sheet.write(row, 15, gd(sreport, sk,
                    age_group, 'abandon', ism), style_value)
        sheet.write(row, 16, gd(sreport, sk,
                    age_group, 'not_responding', ism), style_value)
        sheet.write(row, 17, gd(sreport, sk,
                    age_group, 'total_out', ism), style_value)
        sheet.write(row, 18, gd(sreport, sk,
                    age_group, 'total_out_m', ism), style_value)
        sheet.write(row, 19, gd(sreport, sk,
                    age_group, 'total_out_f', ism), style_value)
        sheet.write(row, 20, gd(sreport, sk,
                    age_group, 'referred', ism), style_value)
        sheet.write(row, 21, gd(sreport, sk,
                    age_group, 'grand_total_out', ism), style_value,)
        sheet.write(row, 22, gd(sreport, sk,
                    age_group, 'total_end', ism), style_value)
        sheet.write(row, 23, gd(sreport, sk,
                    age_group, 'total_end_m', ism), style_value)
        sheet.write(row, 24, gd(sreport, sk,
                    age_group, 'total_end_f', ism), style_value)
        sheet.write(row, 25, gd(sreport, sk,
                    age_group, 'healed_rate', ism), style_value_pc)
        sheet.write(row, 26, gd(sreport, sk,
                    age_group, 'deceased_rate', ism), style_value_pc)
        sheet.write(row, 27, gd(sreport, sk,
                    age_group, 'abandon_rate', ism), style_value_pc)

        return

    def write_month(sheet, period, expected, start_row, is_sam):
        is_mam = not is_sam
        row = start_row

        print("starting month", period, "on row", row, "sheet", sheet)

        # period name
        period_name = get_periods_str(period) \
            if isinstance(period, list) else text_type(period)
        sheet.write_merge(row, row, 0, 27, period_name)
        row += 1

        # if not expected, just move to next period
        if not expected.arrived_report:
            print("not arrived_report")
            return row

        print("report arrived")

        report = expected.arrived_report()
        print("report", report)

        # URENAM
        if is_mam:
            children = get_children(entity, is_sam=False)
            nb_lines = nb_lines_for(URENAMNutritionR, len(children))
            # UREN NAME
            sheet.write_merge(row, row + nb_lines - 1, 0, 0, "URENAM")

            nb_age_groups = len(URENAMNutritionR.age_groups())
            for child in children:
                sheet.write_merge(row, row + nb_age_groups,
                                  1, 1, text_type(child))
                for age_group in URENAMNutritionR.age_groups():
                    write_line(sheet, child, age_group, report,
                               expected, row, False,  False)
                    row += 1

                # total for child
                write_line(sheet, child, None, report,
                           expected, row, False, False)
                row += 1

            sheet.write_merge(
                row, row + len(URENAMNutritionR.age_groups()), 1, 1, "TOTAL")
            for age_group in URENAMNutritionR.age_groups():
                write_line(sheet, "TOTAL", age_group, report,
                           expected, row, True, True)
                row += 1
            # total for child
            write_line(sheet, "TOTAL", None, report,
                       expected, row, True, True)
            row += 1

        else:
            # URENI first
            children = get_children(entity, is_sam, is_ureni=True)
            nb_lines = nb_lines_for(URENINutritionR, len(children))
            sheet.write_merge(row, row + nb_lines - 1, 0, 0, "URENI")

            nb_age_groups = len(URENINutritionR.age_groups())
            for child in children:
                # entity name spans over all ages + total
                sheet.write_merge(row, row + nb_age_groups,
                                  1, 1, text_type(child))

                for age_group in URENINutritionR.age_groups():
                    write_line(sheet, child, age_group, report,
                               expected, row, True, True)
                    row += 1

                # total for child
                write_line(sheet, child, None, report,
                           expected, row, True, True)
                row += 1

            # TOTAL URENI
            sheet.write_merge(row, row + nb_age_groups, 1, 1, "TOTAL")
            for age_group in URENINutritionR.age_groups():
                write_line(sheet, "TOTAL", age_group, report,
                           expected, row, True, True)
                row += 1
            # TOTAL URENI sub total
            write_line(sheet, "TOTAL", None, report,
                       expected, row, True, True)
            row += 1

            # URENAS
            children = get_children(entity, is_sam, is_ureni=False)
            nb_lines = nb_lines_for(URENASNutritionR, len(children))
            sheet.write_merge(row, row + nb_lines - 1, 0, 0, "URENAS")

            nb_age_groups = len(URENASNutritionR.age_groups())
            for child in children:
                # entity name spans over all ages + total
                sheet.write_merge(row, row + nb_age_groups,
                                  1, 1, text_type(child))

                for age_group in URENASNutritionR.age_groups():
                    write_line(sheet, child, age_group, report,
                               expected, row, True, False)
                    row += 1

                # total for child
                write_line(sheet, child, None, report,
                           expected, row, True, False)
                row += 1

            # TOTAL URENAS
            sheet.write_merge(row, row + nb_age_groups, 1, 1, "TOTAL")
            for age_group in URENASNutritionR.age_groups():
                write_line(sheet, "TOTAL", age_group, report,
                           expected, row, True, False)
                row += 1
            # TOTAL URENAS sub total
            write_line(sheet, "TOTAL", None, report,
                       expected, row, True, False)
            row += 1

            # URENI + URENAS
            age_groups = list(set(URENINutritionR.age_groups() +
                                  URENASNutritionR.age_groups()))
            nb_age_groups = len(age_groups) + 1
            sheet.write_merge(row, row + nb_age_groups - 1, 0, 1,
                              "TOTAL URENI + URENAS")

            for age_group in age_groups:
                write_line(sheet, "TOTAL URENI + URENAS",
                           "sam_{}".format(age_group),
                           report, expected, row, True, None)
                row += 1

            print("*****************************")
            print("*****************************")
            print("*****************************")
            # URENI + URENAS sub total
            write_line(sheet, "TOTAL", None, report,
                       expected, row, True, None)
            row += 1
            print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
            print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
            print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")

        return row

    # prepare sheet for SAM
    if entity.level <= 2 or entity.has_urenas or entity.has_ureni:
        sam_sheet = book.add_sheet(
            "{prefix}{name} {uren}"
            .format(prefix=prefix, name=entity.name, uren="URENI_URENAS"))
        write_header(sam_sheet, "URENI-URENAS")

        row = 7
        for period, expected in periods_expecteds:
            row = write_month(sam_sheet, period, expected, row, True)

        # periods total
        row = write_month(sam_sheet, periods, expected, row, True)

    # prepare sheet for MAM
    if entity.level <= 2 or entity.has_urenam:
        mam_sheet = book.add_sheet(
            "{prefix}{name} {uren}"
            .format(prefix=prefix, name=entity.name, uren="URENAM"))
        write_header(mam_sheet, "URENAM")

        row = 7
        for period, expected in periods_expecteds:
            row = write_month(mam_sheet, period, expected, row, False)

        # periods total
        row = write_month(mam_sheet, periods, expected, row, False)

    # J'agrandi la colonne à trois fois la normale.
    # sheet.col(0).width = 0x0d00 * 3

    stream = StringIO.StringIO()
    book.save(stream)

    return "test.xls", stream
