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
from xlutils.copy import copy as xl_copy

from snisi_core.xls_export import xls_update_value_only, ColorMatcher
from snisi_nutrition import get_domain

logger = logging.getLogger(__name__)

# styles
border_all_regular = xlwt.Borders()
border_all_regular.left = 1
border_all_regular.right = 1
border_all_regular.top = 1
border_all_regular.bottom = 1

font_bold = xlwt.Font()
font_bold.name = "Arial"
font_bold.bold = True
font_bold.height = 10 * 0x14

align_center = xlwt.Alignment()
align_center.horz = xlwt.Alignment.HORZ_CENTER
align_center.vert = xlwt.Alignment.VERT_CENTER
align_center.wrap = 1

color_lightgrey = xlwt.Pattern()
color_lightgrey.pattern = xlwt.Pattern.SOLID_PATTERN
color_lightgrey.pattern_fore_colour = ColorMatcher().match_color_index(
    "192,192,192")

style_value_sum = xlwt.XFStyle()
style_value_sum.alignment = align_center
style_value_sum.borders = border_all_regular
style_value_sum.font = font_bold
style_value_sum.pattern = color_lightgrey


def nutrition_weekly_as_xls(report):
    """ Export les données d'un rapport en xls """

    template_path = os.path.join(get_domain().module_path,
                                 'fixtures', 'template-nutrition-weekly.xls')

    template = open_workbook(template_path, formatting_info=True)
    wb = xl_copy(template)
    sheet = wb.get_sheet(0)
    del(template)

    entity = report.entity.casted()

    if entity.type.slug in ('health_region',
                            'health_district',
                            'health_center'):
        xls_update_value_only(sheet, 1, 2,
                              entity.get_health_region().name)
    if entity.type.slug in ('health_district', 'health_center'):
        xls_update_value_only(sheet, 1, 3,
                              entity.get_health_district().name)
    xls_update_value_only(sheet, 1, 4, report.entity.slug)

    xls_update_value_only(sheet, 5, 2, report.period.casted().strid())
    xls_update_value_only(sheet, 5, 4,
                          report.created_by.get_title_full_name())

    xls_update_value_only(sheet, 1, 7, report.urenam_screening)
    xls_update_value_only(sheet, 3, 7, report.urenam_cases)
    xls_update_value_only(sheet, 5, 7, report.urenam_deaths)
    sheet.write(7, 7, xlwt.Formula("SUM(B{r}:F{r})".format(r=8)),
                style_value_sum)

    xls_update_value_only(sheet, 1, 8, report.urenas_screening)
    xls_update_value_only(sheet, 3, 8, report.urenas_cases)
    xls_update_value_only(sheet, 5, 8, report.urenas_deaths)
    sheet.write(8, 7, xlwt.Formula("SUM(B{r}:F{r})".format(r=9)),
                style_value_sum)

    xls_update_value_only(sheet, 1, 9, report.ureni_screening)
    xls_update_value_only(sheet, 3, 9, report.ureni_cases)
    xls_update_value_only(sheet, 5, 9, report.ureni_deaths)
    sheet.write(9, 7, xlwt.Formula("SUM(B{r}:F{r})".format(r=10)),
                style_value_sum)

    sheet.write(10, 1, xlwt.Formula("SUM(B8:C10)"), style_value_sum)
    sheet.write(10, 3, xlwt.Formula("SUM(D8:E10)"), style_value_sum)
    sheet.write(10, 5, xlwt.Formula("SUM(F8:G10)"), style_value_sum)
    sheet.write(10, 7, xlwt.Formula("SUM(H8:I10)"), style_value_sum)

    stream = StringIO.StringIO()
    wb.save(stream)

    return stream
