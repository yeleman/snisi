#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim: ai ts=4 sts=4 et sw=4 nu

from __future__ import (unicode_literals, absolute_import,
                        division, print_function)
import logging
import StringIO
import os
import xlwt

from xlrd import open_workbook
from xlutils.copy import copy

from snisi_core.xls_export import xls_update_value_only
from snisi_reprohealth import get_domain

logger = logging.getLogger(__name__)

TEMPLATE = os.path.join(get_domain().module_path,
                        'fixtures', 'template-MSIPF.xls')


def pfa_activities_as_xls(report):
    """ Export les données d'un rapport en xls """

    template = open_workbook(TEMPLATE, formatting_info=True)
    copy_week_b = copy(template)
    sh_services = copy_week_b.get_sheet(0)
    sh_financial = copy_week_b.get_sheet(1)
    sh_stocks = copy_week_b.get_sheet(2)
    del(template)

    xls_update_value_only(sh_services, 4, 1,  report.entity.name)
    xls_update_value_only(sh_services, 2, 1,  report.entity.slug)
    xls_update_value_only(sh_services, 2, 2,  report.period.middle().month)
    xls_update_value_only(sh_services, 4, 2,  report.period.middle().year)

    # CAP-providing services
    xls_update_value_only(sh_services, 2, 5,  report.tubal_ligations)
    xls_update_value_only(sh_services, 2, 6,  report.intrauterine_devices)
    xls_update_value_only(sh_services, 2, 7,  report.injections)
    xls_update_value_only(sh_services, 2, 8,  report.pills)
    xls_update_value_only(sh_services, 2, 9,  report.male_condoms)
    xls_update_value_only(sh_services, 2, 10,  report.female_condoms)
    xls_update_value_only(sh_services, 2, 11,  report.emergency_controls)
    xls_update_value_only(sh_services, 2, 12,  report.implants)

    for cpt in range(6, 14):
        xls_update_value_only(sh_services, 3, cpt - 1,
                              xlwt.Formula("B{0} * C{0}".format(cpt)))
    xls_update_value_only(sh_services, 3, 13, xlwt.Formula("SUM($D$6:$D$13)"))

    # Clients related services
    xls_update_value_only(sh_services, 3, 15, report.new_clients)
    xls_update_value_only(sh_services, 3, 16, report.previous_clients)
    xls_update_value_only(sh_services, 3, 17, report.under25_visits)
    xls_update_value_only(sh_services, 3, 18, report.over25_visits)
    xls_update_value_only(sh_services, 3, 19, report.very_first_visits)
    xls_update_value_only(sh_services, 3, 20, report.short_term_method_visits)
    xls_update_value_only(sh_services, 3, 21, report.long_term_method_visits)
    xls_update_value_only(sh_services, 3, 22, report.hiv_counseling_clients)
    xls_update_value_only(sh_services, 3, 23, report.hiv_tests)
    xls_update_value_only(sh_services, 3, 24, report.hiv_positive_results)

    # non-CAP providing services
    xls_update_value_only(sh_services, 3, 26, report.implant_removal)
    xls_update_value_only(sh_services, 3, 27, report.iud_removal)

    # Financial Data
    row = 2
    xls_update_value_only(sh_financial, 1, row,
                          report.intrauterine_devices_qty)
    xls_update_value_only(sh_financial, 2, row,
                          report.intrauterine_devices_price)
    xls_update_value_only(sh_financial, 4, row,
                          report.intrauterine_devices_revenue)
    row += 1
    xls_update_value_only(sh_financial, 1, row, report.implants_qty)
    xls_update_value_only(sh_financial, 2, row, report.implants_price)
    xls_update_value_only(sh_financial, 4, row, report.implants_revenue)
    row += 1
    xls_update_value_only(sh_financial, 1, row, report.injections_qty)
    xls_update_value_only(sh_financial, 2, row, report.injections_price)
    xls_update_value_only(sh_financial, 4, row, report.injections_revenue)
    row += 1
    xls_update_value_only(sh_financial, 1, row, report.pills_qty)
    xls_update_value_only(sh_financial, 2, row, report.pills_price)
    xls_update_value_only(sh_financial, 4, row, report.pills_revenue)
    row += 1
    xls_update_value_only(sh_financial, 1, row, report.male_condoms_qty)
    xls_update_value_only(sh_financial, 2, row, report.male_condoms_price)
    xls_update_value_only(sh_financial, 4, row, report.male_condoms_revenue)
    row += 1
    xls_update_value_only(sh_financial, 1, row, report.female_condoms_qty)
    xls_update_value_only(sh_financial, 2, row, report.female_condoms_price)
    xls_update_value_only(sh_financial, 4, row, report.female_condoms_revenue)
    row += 1
    xls_update_value_only(sh_financial, 1, row, report.hiv_tests_qty)
    xls_update_value_only(sh_financial, 2, row, report.hiv_tests_price)
    xls_update_value_only(sh_financial, 4, row, report.hiv_tests_revenue)
    row += 1
    xls_update_value_only(sh_financial, 1, row, report.iud_removal_qty)
    xls_update_value_only(sh_financial, 2, row, report.iud_removal_price)
    xls_update_value_only(sh_financial, 4, row, report.iud_removal_revenue)
    row += 1
    xls_update_value_only(sh_financial, 1, row, report.implant_removal_qty)
    xls_update_value_only(sh_financial, 2, row, report.implant_removal_price)
    xls_update_value_only(sh_financial, 4, row, report.implant_removal_revenue)

    for cpt in range(3, 12):
        xls_update_value_only(sh_financial, 3, cpt - 1,
                              xlwt.Formula("B{0}*C{0}".format(cpt)))

    xls_update_value_only(sh_financial, 3, 11, xlwt.Formula("SUM($D$3:$D$11)"))
    xls_update_value_only(sh_financial, 4, 11, xlwt.Formula("SUM($E$3:$E$11)"))

    # stock
    row = 2
    xls_update_value_only(sh_stocks, 1, row,
                          report.intrauterine_devices_initial)
    xls_update_value_only(sh_stocks, 2, row,
                          report.intrauterine_devices_received)
    xls_update_value_only(sh_stocks, 3, row, report.intrauterine_devices_used)
    xls_update_value_only(sh_stocks, 4, row, report.intrauterine_devices_lost)
    xls_update_value_only(sh_stocks, 6, row,
                          report.intrauterine_devices_observation)
    row += 1
    xls_update_value_only(sh_stocks, 1, row, report.implants_initial)
    xls_update_value_only(sh_stocks, 2, row, report.implants_received)
    xls_update_value_only(sh_stocks, 3, row, report.implants_used)
    xls_update_value_only(sh_stocks, 4, row, report.implants_lost)
    xls_update_value_only(sh_stocks, 6, row, report.implants_observation)
    row += 1
    xls_update_value_only(sh_stocks, 1, row, report.injections_initial)
    xls_update_value_only(sh_stocks, 2, row, report.injections_received)
    xls_update_value_only(sh_stocks, 3, row, report.injections_used)
    xls_update_value_only(sh_stocks, 4, row, report.injections_lost)
    xls_update_value_only(sh_stocks, 6, row, report.injections_observation)
    row += 1
    xls_update_value_only(sh_stocks, 1, row, report.pills_initial)
    xls_update_value_only(sh_stocks, 2, row, report.pills_received)
    xls_update_value_only(sh_stocks, 3, row, report.pills_used)
    xls_update_value_only(sh_stocks, 4, row, report.pills_lost)
    xls_update_value_only(sh_stocks, 6, row, report.pills_observation)
    row += 1
    xls_update_value_only(sh_stocks, 1, row, report.male_condoms_initial)
    xls_update_value_only(sh_stocks, 2, row, report.male_condoms_received)
    xls_update_value_only(sh_stocks, 3, row, report.male_condoms_used)
    xls_update_value_only(sh_stocks, 4, row, report.male_condoms_lost)
    xls_update_value_only(sh_stocks, 6, row, report.male_condoms_observation)
    row += 1
    xls_update_value_only(sh_stocks, 1, row, report.female_condoms_initial)
    xls_update_value_only(sh_stocks, 2, row, report.female_condoms_received)
    xls_update_value_only(sh_stocks, 3, row, report.female_condoms_used)
    xls_update_value_only(sh_stocks, 4, row, report.female_condoms_lost)
    xls_update_value_only(sh_stocks, 6, row, report.female_condoms_observation)
    row += 1
    xls_update_value_only(sh_stocks, 1, row, report.hiv_tests_initial)
    xls_update_value_only(sh_stocks, 2, row, report.hiv_tests_received)
    xls_update_value_only(sh_stocks, 3, row, report.hiv_tests_used)
    xls_update_value_only(sh_stocks, 4, row, report.hiv_tests_lost)
    xls_update_value_only(sh_stocks, 6, row, report.hiv_tests_observation)
    row += 1
    xls_update_value_only(sh_stocks, 1, row, report.pregnancy_tests_initial)
    xls_update_value_only(sh_stocks, 2, row, report.pregnancy_tests_received)
    xls_update_value_only(sh_stocks, 3, row, report.pregnancy_tests_used)
    xls_update_value_only(sh_stocks, 4, row, report.pregnancy_tests_lost)
    xls_update_value_only(sh_stocks, 6, row,
                          report.pregnancy_tests_observation)

    for cpt in range(3, 11):
        xls_update_value_only(sh_stocks, 5, cpt - 1,
                              xlwt.Formula("B{0}+C{0}-D{0}-E{0}".format(cpt)))

    stream = StringIO.StringIO()
    copy_week_b.save(stream)

    return stream
