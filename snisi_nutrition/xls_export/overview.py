#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim: ai ts=4 sts=4 et sw=4 nu

from __future__ import (unicode_literals, absolute_import,
                        division, print_function)
import logging
import StringIO
import copy
from collections import OrderedDict

from py3compat import text_type
import xlwt

from snisi_core.models.Entities import Entity
from snisi_core.models.Projects import Cluster
from snisi_core.models.Reporting import ExpectedReporting
from snisi_core.xls_export import (ColorMatcher, ALPHABET,
                                   xl_set_col_width, xl_set_row_height)
from snisi_tools.datetime import get_periods_str
from snisi_nutrition import period_is_complete
from snisi_nutrition.models.URENAM import URENAMNutritionR
from snisi_nutrition.models.URENI import URENINutritionR
from snisi_nutrition.models.URENAS import URENASNutritionR
from snisi_nutrition.models.Common import AbstractURENutritionR

logger = logging.getLogger(__name__)

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

border_all_large = xlwt.Borders()
border_all_large.left = 2
border_all_large.right = 2
border_all_large.top = 2
border_all_large.bottom = 2

font_regular = xlwt.Font()
font_regular.name = "Trebuchet MS"
font_regular.bold = False
font_regular.height = 12 * 0x14

font_bold = xlwt.Font()
font_bold.name = "Trebuchet MS"
font_bold.bold = True
font_bold.height = 12 * 0x14

font_title = xlwt.Font()
font_title.name = "Trebuchet MS"
font_title.bold = True
font_title.height = 16 * 0x14

align_center = xlwt.Alignment()
align_center.horz = xlwt.Alignment.HORZ_CENTER
align_center.vert = xlwt.Alignment.VERT_CENTER
align_center.wrap = 1

align_left = xlwt.Alignment()
align_left.horz = xlwt.Alignment.HORZ_LEFT
align_left.vert = xlwt.Alignment.VERT_CENTER

align_uren = xlwt.Alignment()
align_uren.horz = xlwt.Alignment.HORZ_CENTER
align_uren.vert = xlwt.Alignment.VERT_CENTER
align_uren.rota = 90

color_empty = xlwt.Pattern()
color_empty.pattern = xlwt.Pattern.SOLID_PATTERN
color_empty.pattern_fore_colour = ColorMatcher().match_color_index("0,0,0")

color_turquoize = xlwt.Pattern()
color_turquoize.pattern = xlwt.Pattern.SOLID_PATTERN
color_turquoize.pattern_fore_colour = ColorMatcher().match_color_index(
    "0,255,255")

color_lightgrey = xlwt.Pattern()
color_lightgrey.pattern = xlwt.Pattern.SOLID_PATTERN
color_lightgrey.pattern_fore_colour = ColorMatcher().match_color_index(
    "192,192,192")

color_darkgrey = xlwt.Pattern()
color_darkgrey.pattern = xlwt.Pattern.SOLID_PATTERN
color_darkgrey.pattern_fore_colour = ColorMatcher().match_color_index(
    "128,128,128")

style_title = xlwt.XFStyle()
style_title.alignment = align_center
style_title.borders = border_bottom_large
style_title.font = font_title

style_label = xlwt.XFStyle()
style_label.alignment = align_left
style_label.borders = border_all_regular
style_label.font = font_regular

style_header = copy.deepcopy(style_label)
style_header.alignment = align_center
style_header.font = font_bold

style_value = xlwt.XFStyle()
style_value.alignment = align_center
style_value.borders = border_all_regular
style_value.font = font_regular

style_value_pc = xlwt.XFStyle()
style_value_pc.alignment = align_center
style_value_pc.borders = border_all_regular
style_value_pc.font = font_regular
style_value_pc.num_format_str = '0%'
style_value_pc.pattern = color_lightgrey

style_value_sum = copy.deepcopy(style_value)
style_value_sum.pattern = color_lightgrey

style_value_pc_sum = copy.deepcopy(style_value_pc)
style_value_pc_sum.pattern = color_lightgrey

style_period = xlwt.XFStyle()
style_period.alignment = align_left
style_period.borders = border_all_large
style_period.font = font_bold
style_period.pattern = color_darkgrey

style_label_uren = copy.deepcopy(style_label)
style_label_uren.alignment = align_uren
style_label_uren.pattern = color_lightgrey

style_label_uren2 = copy.deepcopy(style_label_uren)
style_label_uren2.alignment = align_left
style_label_uren2.pattern = color_turquoize

style_value_uren2 = copy.deepcopy(style_value)
style_value_uren2.pattern = color_turquoize

style_value_pc_uren2 = copy.deepcopy(style_value_pc)
style_value_pc_uren2.pattern = color_turquoize


def write_header(sheet, uren, periods):
    """ writes standard header columns to sheet (SAM/MAM are identical) """

    # main title, all width
    sheet.write_merge(
        0, 0, 0, 27, "RAPPORTS STATISTIQUES MENSUEL - {uren} {periods}"
                     .format(uren=uren, periods=get_periods_str(periods)),
        style_title)

    # empty line folowing

    # first line of headers (mostly merged)
    sheet.write_merge(2, 3, 3, 5, "TOTAL DÉBUT DU MOIS", style_header)

    sheet.write_merge(2, 2, 6, 12, "ADMISSIONS", style_header)

    sheet.write_merge(2, 2, 13, 21, "SORTIES", style_header)

    sheet.write_merge(2, 3, 22, 24, "TOTAL FIN DU MOIS", style_header)

    sheet.write_merge(2, 3, 25, 27, "INDICATEURS DE PERFORMANCE",
                      style_header)

    # second line of headers
    sheet.write_merge(3, 6, 6, 6, "Nouveaux cas", style_header)

    sheet.write_merge(3, 6, 7, 7, "Re-admissions", style_header)

    sheet.write_merge(3, 4, 8, 10, "Total Admissions", style_header)

    sheet.write_merge(3, 6, 11, 11, "Transfert/ Ref. de l' URENI / URENAS",
                      style_header)

    sheet.write_merge(3, 6, 12, 12,
                      "TOTAL ADM GENERAL "
                      "(total adm + Transf. Nut)", style_header)

    sheet.write_merge(3, 6, 13, 13, "Guéris/ Traités avec succès",
                      style_header)

    sheet.write_merge(3, 6, 14, 14, "Décès", style_header)

    sheet.write_merge(3, 6, 15, 15, "Abandons", style_header)

    sheet.write_merge(3, 6, 16, 16, "NR", style_header)

    sheet.write_merge(3, 3, 17, 19, "Total Sorties", style_header)

    sheet.write_merge(3, 6, 20, 20, "Réf. vers URENI/ transfert URENAS",
                      style_header)

    sheet.write_merge(3, 6, 21, 21,
                      "TOTAL SORTIE GNL (Tot sorties + Réf/Tr)",
                      style_header)

    # third line of headers
    sheet.write_merge(4, 6, 17, 17, "Total", style_header)
    sheet.write_merge(4, 6, 18, 18, "M", style_header)
    sheet.write_merge(4, 6, 19, 19, "F", style_header)

    sheet.write_merge(4, 6, 22, 22, "Total fin du mois", style_header)

    sheet.write_merge(4, 6, 23, 23, "M", style_header)

    sheet.write_merge(4, 6, 24, 24, "F", style_header)

    sheet.write_merge(4, 6, 25, 25, "% Guérison", style_header)
    sheet.write_merge(4, 6, 26, 26, "% Décès", style_header)
    sheet.write_merge(4, 6, 27, 27, "% Abandons", style_header)

    # fourth line of headers
    sheet.write_merge(5, 6, 1, 1, "NOM DE LA STRUCTURE", style_header)
    sheet.write_merge(5, 6, 2, 2, "Catégorie d'age", style_header)

    sheet.write_merge(4, 6, 3, 3, "Total", style_header)
    sheet.write_merge(4, 6, 4, 4, "M", style_header)
    sheet.write_merge(4, 6, 5, 5, "F", style_header)

    sheet.write_merge(5, 6, 8, 8, "Total", style_header)
    sheet.write_merge(5, 6, 9, 9, "M", style_header)
    sheet.write_merge(5, 6, 10, 10, "F", style_header)

    # set columns width
    xl_set_col_width(sheet, 0, 2.82)
    xl_set_col_width(sheet, 1, 9)
    xl_set_col_width(sheet, 2, 2.93)
    xl_set_col_width(sheet, 3, 2.29)
    xl_set_col_width(sheet, 4, 1.9)
    xl_set_col_width(sheet, 5, 1.94)
    xl_set_col_width(sheet, 6, 2.54)
    xl_set_col_width(sheet, 7, 2.65)
    xl_set_col_width(sheet, 8, 2.33)
    xl_set_col_width(sheet, 9, 1.8)
    xl_set_col_width(sheet, 10, 1.94)
    xl_set_col_width(sheet, 11, 3.42)
    xl_set_col_width(sheet, 12, 3.39)
    xl_set_col_width(sheet, 13, 2.26)
    xl_set_col_width(sheet, 14, 2.01)
    xl_set_col_width(sheet, 15, 2.54)
    xl_set_col_width(sheet, 16, 2.12)
    xl_set_col_width(sheet, 17, 2.12)
    xl_set_col_width(sheet, 18, 2.05)
    xl_set_col_width(sheet, 19, 1.98)
    xl_set_col_width(sheet, 20, 2.33)
    xl_set_col_width(sheet, 21, 3.85)
    xl_set_col_width(sheet, 22, 2.43)
    xl_set_col_width(sheet, 23, 1.94)
    xl_set_col_width(sheet, 24, 1.98)
    xl_set_col_width(sheet, 25, 2.54)
    xl_set_col_width(sheet, 26, 2.29)
    xl_set_col_width(sheet, 27, 2.43)

    # set row height
    xl_set_row_height(sheet, 0, 0.74)
    xl_set_row_height(sheet, 1, 0.56)
    xl_set_row_height(sheet, 2, 0.53)
    xl_set_row_height(sheet, 3, 0.56)
    xl_set_row_height(sheet, 4, 1.03)
    xl_set_row_height(sheet, 5, 0.61)
    xl_set_row_height(sheet, 6, 1.19)


def write_month(sheet, period, entity, expected, start_row, is_sam):
    is_mam = not is_sam  # shortcut
    row = start_row  # counter

    # write a line containing only period name
    period_name = get_periods_str(period) \
        if isinstance(period, list) else text_type(period)
    sheet.write_merge(row, row, 0, 27, period_name.upper(), style_period)

    # update row size for period name
    xl_set_row_height(sheet, row, 0.69)

    # update row count
    row += 1

    # if not expected, just move to next period
    if expected is None or not expected.arrived_report:
        return row

    report = expected.arrived_report()

    # URENAM
    if is_mam:
        children = get_children(entity, is_sam=False)
        nb_lines = nb_lines_for(URENAMNutritionR, len(children))

        # write URENAM (vertical merge)
        sheet.write_merge(row, row + nb_lines - 1, 0, 0,
                          "URENAM", style_label_uren)

        age_groups = URENAMNutritionR.age_groups()
        nb_age_groups = len(age_groups)

        for child in children:

            # write entity name (spans over all ages + total)
            sheet.write_merge(row, row + nb_age_groups,
                              1, 1, text_type(child), style_label)

            for age_group in URENAMNutritionR.age_groups():

                # write line for this age group
                write_line(sheet, child, children, age_group, age_groups,
                           report, expected, row, False,  False)
                row += 1

            # write line for the total of all age group at this entity
            write_line(sheet, child, children, None, age_groups,
                       report, expected, row, False, False)
            row += 1

        # write summary of all children for that period (for each age group)
        sheet.write_merge(
            row, row + len(URENAMNutritionR.age_groups()), 1, 1,
            "TOTAL", style_label)

        for age_group in URENAMNutritionR.age_groups():

            # write line for this age group
            write_line(sheet, "TOTAL", children, age_group, age_groups,
                       report, expected, row, True, True)
            row += 1

        # write line for the total of all age group at this entity
        write_line(sheet, "TOTAL", children, None, age_groups,
                   report, expected, row, True, True)
        row += 1

    else:
        # SAM sheet contains URENI alone first then URENAS alone

        ###
        # URENI
        ###

        children = get_children(entity, is_sam, is_ureni=True)
        nb_lines = nb_lines_for(URENINutritionR, len(children))
        nb_ureni_children = len(children)

        # write URENI (vertical merge)
        sheet.write_merge(row, row + nb_lines - 1, 0, 0,
                          "URENI", style_label_uren)

        age_groups = URENINutritionR.age_groups()
        nb_age_groups = len(age_groups)

        for child in children:

            # entity name spans over all ages + total
            sheet.write_merge(row, row + nb_age_groups,
                              1, 1, text_type(child), style_label)

            for age_group in URENINutritionR.age_groups():

                # write line for this age group
                write_line(sheet, child, children, age_group, age_groups,
                           report, expected, row, True, True)
                row += 1

            # write line for the total of all age group at this entity
            write_line(sheet, child, children, None, age_groups,
                       report, expected, row, True, True)
            row += 1

        # write summary of all children for that period (for each age group)
        sheet.write_merge(row, row + nb_age_groups, 1, 1,
                          "TOTAL", style_label)

        for age_group in URENINutritionR.age_groups():

            # write line for this age group
            write_line(sheet, "TOTAL", children, age_group, age_groups,
                       report, expected, row, True, True)
            row += 1

        # write line for the total of all age group at this entity
        write_line(sheet, "TOTAL", children, None, age_groups,
                   report, expected, row, True, True)
        row += 1

        ###
        # URENAS
        ###

        children = get_children(entity, is_sam, is_ureni=False)
        nb_lines = nb_lines_for(URENASNutritionR, len(children))
        nb_urenas_children = len(children)

        # write URENAS (vertical merge)
        sheet.write_merge(row, row + nb_lines - 1, 0, 0,
                          "URENAS", style_label_uren)

        age_groups = URENASNutritionR.age_groups()
        nb_age_groups = len(age_groups)

        for child in children:

            # entity name spans over all ages + total
            sheet.write_merge(row, row + nb_age_groups,
                              1, 1, text_type(child), style_label)

            for age_group in URENASNutritionR.age_groups():

                # write line for this age group
                write_line(sheet, child, children, age_group, age_groups,
                           report, expected, row, True, False)
                row += 1

            # write line for the total of all age group at this entity
            write_line(sheet, child, children, None, age_groups,
                       report, expected, row, True, False)
            row += 1

        # write summary of all children for that period (for each age group)
        sheet.write_merge(row, row + nb_age_groups, 1, 1,
                          "TOTAL", style_label)

        for age_group in age_groups:

            # write line for this age group
            write_line(sheet, "TOTAL", children, age_group, age_groups,
                       report, expected, row, True, False)
            row += 1

        # write line for the total of all age group at this entity
        write_line(sheet, "TOTAL", children, None, age_groups,
                   report, expected, row, True, False)
        row += 1

        ###
        # URENI + URENAS
        ###

        age_groups = list(OrderedDict.fromkeys(
            URENINutritionR.age_groups()
            + URENASNutritionR.age_groups()))
        nb_age_groups = len(age_groups) + 1

        # write URENI + URENAS (vertical merge)
        sheet.write_merge(row, row + nb_age_groups - 1, 0, 1,
                          "TOTAL URENI + URENAS", style_label_uren2)

        for age_group in age_groups:

            # write line for this age group
            write_line(sheet, "TOTAL URENI + URENAS", children,
                       "sam_{}".format(age_group), age_groups,
                       report, expected, row, True, None,
                       nb_ureni_children=nb_ureni_children,
                       nb_ureni_age_groups=len(URENINutritionR.age_groups()),
                       nb_urenas_children=nb_urenas_children,
                       nb_urenas_age_groups=len(URENASNutritionR.age_groups()))
            row += 1

        # write line for the total of all age group at this entity
        write_line(sheet, "TOTAL", children, None, age_groups,
                   report, expected, row, True, None,
                   nb_ureni_children=nb_ureni_children,
                   nb_ureni_age_groups=len(URENINutritionR.age_groups()),
                   nb_urenas_children=nb_urenas_children,
                   nb_urenas_age_groups=len(URENASNutritionR.age_groups()))
        row += 1

    return row


def write_line(sheet, child, children, age_group, age_groups,
               report, expected, row, is_sam, is_ureni,
               nb_ureni_children=None, nb_ureni_age_groups=None,
               nb_urenas_children=None, nb_urenas_age_groups=None,
               ):

    # whether line is part of a children-wide total
    is_total = not isinstance(child, Entity)

    is_ureni_plus_urenas = is_sam and is_ureni is None

    # styles definitions changes for total rows and URENI + URENAS
    if is_sam and is_ureni is None:
        sv = style_value_uren2
        svpc = style_value_pc_uren2
        svs = style_value_uren2
        sl = style_label_uren2
    else:
        sv = style_value
        svpc = style_value_pc
        svs = style_value_sum
        sl = style_label
        if is_total or age_group is None:
            sv = style_value_sum
            svpc = style_value_pc_sum

    # our default row height
    xl_set_row_height(sheet, row, 0.64)

    # first column is age group name (or Total)
    if age_group is None:
        age_group_name = "Total"
    else:
        age_group_name = AbstractURENutritionR.AGE_LABELS.get(
            age_group.replace("sam_", ""), age_group)
    sheet.write(row, 2, age_group_name, sl)

    # retrieve data holder (montly report or sub report)
    if is_total:
        sreport = report
    else:
        # grab report for that location if exist
        try:
            sreport = [r for r in report.direct_sources()
                       if r.entity.slug == child.slug][0]
        except (IndexError, AttributeError):
            sreport = None

    # if no report, leave all fields blank and move to next
    if sreport is None:
        return

    def gd(report, sk, age_group, field, is_sam=False):
        """ shortcut to select field on specified report """
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

    # intermediate variables
    xlrow = row + 1  # visual row number (1-indexed)
    ism = is_sam
    istr = age_group is None  # is total row ?
    nb_children = len(children)
    sk = 'm'  # sub-report key

    if is_sam:
        sk = 'i' if is_ureni else 'a'
        if is_total and is_ureni is None:
            sk = None
        if age_group is None:
            age_group

    def colsum(letter):
        """ SUM formula for a column based on age groups """

        r1 = xlrow - len(age_groups)
        r2 = xlrow - 1
        return xlwt.Formula("SUM({l}{r1}:{l}{r2})"
                            .format(l=letter, r1=r1, r2=r2))

    def wr(col, field, s=sv):
        """ writes line for a regular field (ie: not sum)

            either gets the sum of the column's age if total
            or retrieve data from report """

        if is_total:

            if is_ureni_plus_urenas:

                age_rows = []

                # total for URENI + URENAS
                if age_group is None:
                    age_rows = range(xlrow - len(age_groups), xlrow)
                else:
                    cage_group = age_group.replace('sam_', '')
                    ureni_age_groups = URENINutritionR.age_groups()
                    urenas_age_groups = URENASNutritionR.age_groups()

                    offset = age_groups.index(cage_group)
                    start = xlrow - offset

                    if cage_group in ureni_age_groups:
                        ureni_offset = list(reversed(ureni_age_groups)) \
                            .index(cage_group) + 2
                        ureni_sum = (
                            start - ((nb_urenas_children + 1)
                                     * (len(urenas_age_groups) + 1))
                            - ureni_offset)
                        age_rows.append(ureni_sum)

                    if cage_group in urenas_age_groups:
                        urenas_offset = list(reversed(urenas_age_groups)) \
                            .index(cage_group) + 2
                        urenas_sum = start - urenas_offset
                        age_rows.append(urenas_sum)
            else:
                nb_age_groups2 = len(age_groups) + 1
                first_row = xlrow - nb_children * nb_age_groups2
                age_rows = [first_row + i * nb_age_groups2
                            for i in range(nb_children)]

            fmt = "SUM({})".format(",".join(["{c}{r}".format(c=col, r=r)
                                             for r in age_rows]))
            data = xlwt.Formula(fmt)
        else:
            data = colsum(col) if istr \
                else gd(sreport, sk, age_group, field, ism)
        sheet.write(row, ALPHABET.index(col), data, s)

    def wsr(col, *sumcols):
        """ inside-row column's sum for sex breakdowns """
        data = xlwt.Formula("SUM({})".format(
            ",".join(["{cc}{r}".format(r=xlrow, cc=cc)
                      for cc in sumcols])))
        sheet.write(row, ALPHABET.index(col), data, svs)

    # total_start
    wsr("D", 'E', 'F')
    wr("E", 'total_start_m')
    wr("F", 'total_start_f')

    wr("G", 'new_cases')
    wr("H", 'returned')

    # total_in
    wsr("I", 'J', 'K')

    wr("J", 'total_in_m')
    wr("K", 'total_in_f')
    wr("L", 'transferred')

    # grand_total_in
    wsr("M", 'I', 'L')

    wr("N", 'healed')
    wr("O", 'deceased')
    wr("P", 'abandon')
    wr("Q", 'not_responding')

    # total_out
    wsr("R", 'S', 'T')
    wr("S", 'total_out_m')
    wr("T", 'total_out_f')

    wr("U", 'referred')

    # grand_total_out
    wsr("V", 'R', 'U')

    wsr("W", 'X', 'Y')
    wr("X", 'total_end_m')
    wr("Y", 'total_end_f')

    # healed_rate = gd(sreport, sk, age_group, 'healed_rate', ism)
    healed_rate = xlwt.Formula(
        'IF(SUM(N{r}:P{r})=0,"-",N{r}/SUM(N{r}:P{r}))'.format(r=xlrow))
    sheet.write(row, 25, healed_rate, svpc)

    # deceased_rate = gd(sreport, sk, age_group, 'deceased_rate', ism)
    deceased_rate = xlwt.Formula(
        'IF(SUM(N{r}:P{r})=0,"-",O{r}/SUM(N{r}:P{r}))'.format(r=xlrow))
    sheet.write(row, 26, deceased_rate, svpc)

    # abandon_rate = gd(sreport, sk, age_group, 'abandon_rate', ism)
    abandon_rate = xlwt.Formula(
        'IF(SUM(N{r}:P{r})=0,"-",P{r}/SUM(N{r}:P{r}))'.format(r=xlrow))
    sheet.write(row, 27, abandon_rate, svpc)

    return


def get_children(entity, is_sam, is_ureni=None):

    def hc_filter(hc, is_sam, is_ureni):
        if is_sam:
            return hc.has_ureni if is_ureni else hc.has_urenas
        else:
            return hc.has_urenam
    if entity.type.slug == 'health_district':
        return [e for e in entity.get_health_centers()
                if hc_filter(e, is_sam, is_ureni)]
    elif entity.type.slug == 'health_region':
        return entity.get_health_districts()
    elif entity.type.slug == 'country':
        return entity.get_health_regions()


def nb_lines_for(reportcls, nb_children):
    # each child (entity) has a line for each age group
    # plus one line for total
    # then a total for each age group
    # ending with a final total line
    nb_age_groups = len(reportcls.age_groups())
    return (nb_age_groups + 1) * nb_children + nb_age_groups + 1


def nutrition_overview_xls(entity, periods, is_sam=False, is_mam=False):
    """ Exports complete SAM/MAM Overview data as XLS

        SAM Report is exported in one sheet
        MAM Report is exported in one sheet

        Both sheets list all entities data for each month for all ages
        then followed by a summary for the whole period """

    # compute all the data. XLS is just a display of this
    cluster = Cluster.get_or_none('nutrition_routine')
    report_classes = cluster.domain \
        .import_from('expected.report_classes_for')(cluster)

    periods_expecteds = [
        (period, ExpectedReporting.objects.filter(
            period=period, entity=entity,
            report_class__in=report_classes).last())
        for period in periods if period_is_complete(period, entity)
    ]

    # build sheet's prefix
    prefix = {
        'health_district': "DS",
        'health_region': "DRS"
    }.get(entity.type.slug, "")
    if prefix:
        prefix += " "

    # excel file spreadsheet holder (workbook)
    book = xlwt.Workbook(encoding='utf-8')

    # create SAM sheet
    if entity.level <= 2 or entity.has_urenas or entity.has_ureni:

        sam_sheet = book.add_sheet(
            "{prefix}{name} {uren}"
            .format(prefix=prefix, name=entity.name, uren="URENI_URENAS"))

        # default sheet zoom is 60%
        sam_sheet.normal_magn = 60

        # header is 7 rows wide
        write_header(sam_sheet, "URENI-URENAS", periods)
        row = 7

        # loop through periods to write data lines
        for period, expected in periods_expecteds:
            row = write_month(sam_sheet, period, entity, expected, row, True)

        # write all-periods summary
        row = write_month(sam_sheet, periods, entity, None, row, True)

    # create MAM sheet
    if entity.level <= 2 or entity.has_urenam:

        mam_sheet = book.add_sheet(
            "{prefix}{name} {uren}"
            .format(prefix=prefix, name=entity.name, uren="URENAM"))

        # default sheet zoom is 60%
        mam_sheet.normal_magn = 60

        # header is 7 rows wide
        write_header(mam_sheet, "URENAM", periods)
        row = 7

        # loop through periods to write data lines
        for period, expected in periods_expecteds:
            row = write_month(mam_sheet, period, entity, expected, row, False)

        # write all-periods summary
        row = write_month(mam_sheet, periods, entity, None, row, False)

    stream = StringIO.StringIO()
    book.save(stream)

    filename = "Rapport MAS-MAM {}.xls".format(get_periods_str(periods))

    return filename, stream
