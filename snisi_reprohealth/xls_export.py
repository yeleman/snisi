#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim: ai ts=4 sts=4 et sw=4 nu

from __future__ import (unicode_literals, absolute_import,
                        division, print_function)
import logging
import StringIO

from xlrd import open_workbook
from xlutils.copy import copy
import xlwt

logger = logging.getLogger(__name__)

TEMPLATE = "snisi_reprohealth/fixtures/template-MSIPF.xls"

# Définition des bordures
borders = xlwt.Borders()
borders.left = 1
borders.right = 1
borders.top = 1
borders.bottom = 1

# couleurs
color = xlwt.Pattern()
color.pattern = xlwt.Pattern.SOLID_PATTERN
color.pattern_fore_colour = 42
balance_color = xlwt.Pattern()
balance_color.pattern = xlwt.Pattern.SOLID_PATTERN
balance_color.pattern_fore_colour = 23

# On définit l'alignement
alcenter = xlwt.Alignment()
alcenter.horz = xlwt.Alignment.HORZ_CENTER
alcenter.vert = xlwt.Alignment.VERT_CENTER

# Styles
style = xlwt.XFStyle()
style.borders = borders
style.pattern = color
style.alignment = alcenter

balance_style = xlwt.XFStyle()
balance_style.borders = borders
balance_style.pattern = balance_color
balance_style.alignment = alcenter

b_style = xlwt.XFStyle()
b_style.borders = borders
b_style.alignment = alcenter
b_style.num_format_str = '0.0'

observation_style = xlwt.XFStyle()
observation_style.borders = borders
observation_style.pattern = color


def pfa_activities_as_xls(report):
    """ Export les données d'un rapport en xls """

    template = open_workbook(TEMPLATE, formatting_info=True)
    copy_week_b = copy(template)
    sh_services = copy_week_b.get_sheet(0)
    sh_financial = copy_week_b.get_sheet(1)
    sh_stocks = copy_week_b.get_sheet(2)

    sh_services.write(1, 4, report.entity.name, style)
    sh_services.write(1, 2, report.entity.slug, style)
    sh_services.write(2, 2, report.period.middle().month, style)
    sh_services.write(2, 4, report.period.middle().year, style)

    # CAP-providing services
    sh_services.write(5, 2, report.tubal_ligations, style)
    sh_services.write(6, 2, report.intrauterine_devices, style)
    sh_services.write(7, 2, report.injections, style)
    sh_services.write(8, 2, report.pills, style)
    sh_services.write(9, 2, report.male_condoms, style)
    sh_services.write(10, 2, report.female_condoms, style)
    sh_services.write(11, 2, report.emergency_controls, style)
    sh_services.write(12, 2, report.implants, style)

    for cpt in range(6, 14):
        sh_services.write(cpt - 1, 3, xlwt.Formula("B{0} * C{0}".format(cpt)),
                          b_style)
    sh_services.write(13, 3, xlwt.Formula("SUM($D$6:$D$13)"), b_style)

    # Clients related services
    sh_services.write(15, 3, report.new_clients, style)
    sh_services.write(16, 3, report.previous_clients, style)
    sh_services.write(17, 3, report.under25_visits, style)
    sh_services.write(18, 3, report.over25_visits, style)
    sh_services.write(19, 3, report.very_first_visits, style)
    sh_services.write(20, 3, report.short_term_method_visits, style)
    sh_services.write(21, 3, report.long_term_method_visits, style)
    sh_services.write(22, 3, report.hiv_counseling_clients, style)
    sh_services.write(23, 3, report.hiv_tests, style)
    sh_services.write(24, 3, report.hiv_positive_results, style)

    # non-CAP providing services
    sh_services.write(26, 3, report.implant_removal, style)
    sh_services.write(27, 3, report.iud_removal, style)

    # Financial Data
    row = 2
    sh_financial.write(row, 1, report.intrauterine_devices_qty, style)
    sh_financial.write(row, 2, report.intrauterine_devices_price, style)
    sh_financial.write(row, 4, report.intrauterine_devices_revenue, style)
    row += 1
    sh_financial.write(row, 1, report.implants_qty, style)
    sh_financial.write(row, 2, report.implants_price, style)
    sh_financial.write(row, 4, report.implants_revenue, style)
    row += 1
    sh_financial.write(row, 1, report.injections_qty, style)
    sh_financial.write(row, 2, report.injections_price, style)
    sh_financial.write(row, 4, report.injections_revenue, style)
    row += 1
    sh_financial.write(row, 1, report.pills_qty, style)
    sh_financial.write(row, 2, report.pills_price, style)
    sh_financial.write(row, 4, report.pills_revenue, style)
    row += 1
    sh_financial.write(row, 1, report.male_condoms_qty, style)
    sh_financial.write(row, 2, report.male_condoms_price, style)
    sh_financial.write(row, 4, report.male_condoms_revenue, style)
    row += 1
    sh_financial.write(row, 1, report.female_condoms_qty, style)
    sh_financial.write(row, 2, report.female_condoms_price, style)
    sh_financial.write(row, 4, report.female_condoms_revenue, style)
    row += 1
    sh_financial.write(row, 1, report.hiv_tests_qty, style)
    sh_financial.write(row, 2, report.hiv_tests_price, style)
    sh_financial.write(row, 4, report.hiv_tests_revenue, style)
    row += 1
    sh_financial.write(row, 1, report.iud_removal_qty, style)
    sh_financial.write(row, 2, report.iud_removal_price, style)
    sh_financial.write(row, 4, report.iud_removal_revenue, style)
    row += 1
    sh_financial.write(row, 1, report.implant_removal_qty, style)
    sh_financial.write(row, 2, report.implant_removal_price, style)
    sh_financial.write(row, 4, report.implant_removal_revenue, style)

    for cpt in range(3, 12):
        sh_financial.write(cpt - 1, 3, xlwt.Formula("B{0}*C{0}".format(cpt)),
                           balance_style)

    sh_financial.write(11, 3, xlwt.Formula("SUM($D$3:$D$11)"), balance_style)
    sh_financial.write(11, 4, xlwt.Formula("SUM($E$3:$E$11)"), balance_style)

    # stock
    row = 2
    sh_stocks.write(row, 1, report.intrauterine_devices_initial, style)
    sh_stocks.write(row, 2, report.intrauterine_devices_received, style)
    sh_stocks.write(row, 3, report.intrauterine_devices_used, style)
    sh_stocks.write(row, 4, report.intrauterine_devices_lost, style)
    sh_stocks.write(row, 6, report.intrauterine_devices_observation,
                    observation_style)
    row += 1
    sh_stocks.write(row, 1, report.implants_initial, style)
    sh_stocks.write(row, 2, report.implants_received, style)
    sh_stocks.write(row, 3, report.implants_used, style)
    sh_stocks.write(row, 4, report.implants_lost, style)
    sh_stocks.write(row, 6, report.implants_observation, observation_style)
    row += 1
    sh_stocks.write(row, 1, report.injections_initial, style)
    sh_stocks.write(row, 2, report.injections_received, style)
    sh_stocks.write(row, 3, report.injections_used, style)
    sh_stocks.write(row, 4, report.injections_lost, style)
    sh_stocks.write(row, 6, report.injections_observation, observation_style)
    row += 1
    sh_stocks.write(row, 1, report.pills_initial, style)
    sh_stocks.write(row, 2, report.pills_received, style)
    sh_stocks.write(row, 3, report.pills_used, style)
    sh_stocks.write(row, 4, report.pills_lost, style)
    sh_stocks.write(row, 6, report.pills_observation, observation_style)
    row += 1
    sh_stocks.write(row, 1, report.male_condoms_initial, style)
    sh_stocks.write(row, 2, report.male_condoms_received, style)
    sh_stocks.write(row, 3, report.male_condoms_used, style)
    sh_stocks.write(row, 4, report.male_condoms_lost, style)
    sh_stocks.write(row, 6, report.male_condoms_observation, observation_style)
    row += 1
    sh_stocks.write(row, 1, report.female_condoms_initial, style)
    sh_stocks.write(row, 2, report.female_condoms_received, style)
    sh_stocks.write(row, 3, report.female_condoms_used, style)
    sh_stocks.write(row, 4, report.female_condoms_lost, style)
    sh_stocks.write(row, 6, report.female_condoms_observation,
                    observation_style)
    row += 1
    sh_stocks.write(row, 1, report.hiv_tests_initial, style)
    sh_stocks.write(row, 2, report.hiv_tests_received, style)
    sh_stocks.write(row, 3, report.hiv_tests_used, style)
    sh_stocks.write(row, 4, report.hiv_tests_lost, style)
    sh_stocks.write(row, 6, report.hiv_tests_observation, observation_style)
    row += 1
    sh_stocks.write(row, 1, report.pregnancy_tests_initial, style)
    sh_stocks.write(row, 2, report.pregnancy_tests_received, style)
    sh_stocks.write(row, 3, report.pregnancy_tests_used, style)
    sh_stocks.write(row, 4, report.pregnancy_tests_lost, style)
    sh_stocks.write(row, 6, report.pregnancy_tests_observation,
                    observation_style)

    for cpt in range(3, 11):
        sh_stocks.write(cpt - 1, 5,
                        xlwt.Formula("B{0}+C{0}-D{0}-E{0}".format(cpt)),
                        balance_style)

    # Pour le teste
    name_file = '{name_file}.xls'.format(name_file="test_export")
    copy_week_b.save(name_file)

    stream = StringIO.StringIO()
    copy_week_b.save(stream)

    return stream
