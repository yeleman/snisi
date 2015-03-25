#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim: ai ts=4 sts=4 et sw=4 nu

from __future__ import (unicode_literals, absolute_import,
                        division, print_function)
import logging
import StringIO
import os

from xlrd import open_workbook
from xlutils.copy import copy as xl_copy

from snisi_core.xls_export import xls_update_value_only
from snisi_nutrition import get_domain

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
        xls_update_value_only(sheet, colB, 2, report.period.middle().month)
        xls_update_value_only(sheet, colB, 3, report.period.middle().year)
        xls_update_value_only(sheet, colA, 3,
                              report.entity.display_short_health_hierarchy())
        xls_update_value_only(sheet, colA, 4, report.entity.slug)
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
