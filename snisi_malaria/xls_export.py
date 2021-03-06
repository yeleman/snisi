#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim: ai ts=4 sts=4 et sw=4 nu

from __future__ import (unicode_literals, absolute_import,
                        division, print_function)
import StringIO
import os
import xlwt

from py3compat import text_type

from xlrd import open_workbook
from xlutils.copy import copy

from snisi_core.xls_export import xls_update_value_only
from snisi_malaria import get_domain

# Définition des bordures
borders = xlwt.Borders()
borders.left = 1
borders.right = 1
borders.top = 1
borders.bottom = 1

borderformbottom = xlwt.Borders()
borderformbottom.left = 0
borderformbottom.right = 0
borderformbottom.top = 0
borderformbottom.bottom = 2

borderformright = xlwt.Borders()
borderformright.left = 0
borderformright.right = 2
borderformright.top = 0
borderformright.bottom = 2

# Définition du font
font = xlwt.Font()
font.bold = True
font.height = 10 * 0x14

# On définit l'alignement
alcenter = xlwt.Alignment()
alcenter.horz = xlwt.Alignment.HORZ_CENTER
alcenter.vert = xlwt.Alignment.VERT_CENTER

# color
colordescription = xlwt.Pattern()
colordescription.pattern = xlwt.Pattern.SOLID_PATTERN
colordescription.pattern_fore_colour = 44

colordate = xlwt.Pattern()
colordate.pattern = xlwt.Pattern.SOLID_PATTERN
colordate.pattern_fore_colour = 0x01B

colortitle = xlwt.Pattern()
colortitle.pattern = xlwt.Pattern.SOLID_PATTERN
colortitle.pattern_fore_colour = 22

colorvide = xlwt.Pattern()
colorvide.pattern = xlwt.Pattern.SOLID_PATTERN
colorvide.pattern_fore_colour = 8

# style
styledescription = xlwt.XFStyle()
styledescription.pattern = colordescription

stylevariable = xlwt.XFStyle()
stylevariable.borders = borders
stylevariable.alignment = alcenter

styletitle = xlwt.XFStyle()
styletitle.pattern = colortitle
styletitle.borders = borders
styletitle.font = font
styletitle.alignment = alcenter

styledate = xlwt.XFStyle()
styledate.alignment = alcenter
styledate.pattern = colordate
styledate.borders = borders

stylelabel = xlwt.XFStyle()
stylelabel.borders = borders

stylevide = xlwt.XFStyle()
stylevide.pattern = colorvide
stylevide.alignment = alcenter

styleborformbutton = xlwt.XFStyle()
styleborformbutton.borders = borderformbottom

styleborformright = xlwt.XFStyle()
styleborformright.borders = borderformright

styletitleform = xlwt.XFStyle()
styletitleform.alignment = alcenter
styletitleform.borders = borders
styletitleform.font = font

styleentity = xlwt.XFStyle()
styleentity.borders = borders
styleentity.pattern = colortitle
styleentity.font = font


def malaria_monthly_routine_as_xls(report):
    """ Export les données d'un rapport en xls """

    from snisi_core.models.Reporting import PERIODICAL_SOURCE

    def report_status_verbose(value):
        if is_aggregated(report):
            return value
        else:
            for v, name in report.YESNO.items():
                if text_type(v) == value:
                    return text_type(name)
            return value

    def is_aggregated(report):
        return report.REPORTING_TYPE != PERIODICAL_SOURCE

    # On crée le doc xls
    book = xlwt.Workbook(encoding='utf-8')

    # On crée une feuille nommé Report
    sheet = book.add_sheet("Report")

    # J'agrandi la colonne à trois fois la normale.
    sheet.col(0).width = 0x0d00 * 3

    # Principe
    # write((nbre ligne - 1), nbre colonne, "conten", style(optionnel).
    # write_merge((nbre ligne - 1), (nbre ligne - 1) + nbre de ligne
    # à merger, (nbre de colonne - 1), (nbre de colonne - 1) + nbre
    # de colonne à merger, "conten", style(optionnel)).
    if is_aggregated(report):
        sheet.write_merge(0, 0, 0, 12, "Formulaire de Collecte - Données"
                          "sur l'Information de Routime du PNLP - "
                          "Niveau Aggrégé", styletitleform)
    else:
        sheet.write_merge(0, 0, 0, 12, "Formulaire de Collecte - Données"
                          "sur l'Information de Routime du PNLP - "
                          "Niveau Primaire", styletitleform)
    sheet.write(2, 0, "Localité", styledescription)
    sheet.write(3, 0, "Code SNISI", styledescription)

    sheet.write_merge(4, 5, 0, 1, "Classification", styletitle)
    sheet.write_merge(
        6, 6, 0, 1, "Total consultation, toutes causes confondues", stylelabel)
    sheet.write_merge(
        7, 7, 0, 1, "Nbre de Cas de paludisme (Tous suspectés)", stylelabel)
    sheet.write_merge(
        8, 8, 0, 1, "Cas de paludisme testés (GE et/ou TDR)", stylelabel)
    sheet.write_merge(
        9, 9, 0, 1, "Cas de paludisme confirmés (GE et/ou TDR)", stylelabel)
    sheet.write_merge(
        10, 10, 0, 1, "Nbre de Cas de paludisme Simple", stylelabel)
    sheet.write_merge(
        11, 11, 0, 1, "Nbre de Cas de paludisme Grave", stylelabel)
    sheet.write_merge(12, 12, 0, 1, "Nbre de Cas traités avec CTA", stylelabel)
    sheet.write_merge(13, 13, 0, 12, "")

    sheet.write_merge(14, 15, 0, 1, "Classification", styletitle)
    sheet.write_merge(16, 16, 0, 1, "Total Hospitalisations toutes"
                                    "causes confondues", stylelabel)
    sheet.write_merge(17, 17, 0, 1, "Total Hospitalisés Paludisme", stylelabel)
    sheet.write_merge(18, 18, 0, 12, "")

    sheet.write_merge(19, 20, 0, 1, "Classification", styletitle)
    sheet.write_merge(21, 21, 0, 1, "Total cas de décès toutes causes"
                                    "confondues", stylelabel)
    sheet.write_merge(22, 22, 0, 1, "Cas de décès pour paludisme", stylelabel)
    sheet.write_merge(23, 23, 0, 9, "")

    sheet.write_merge(24, 24, 0, 5, "Moustiquaires imprégnées"
                                    "d'insecticide distribuées", styletitle)

    sheet.write_merge(25, 25, 0, 1, "Classification", styletitle)
    sheet.write_merge(26, 26, 0, 1, "Nombre de moustiquaires"
                                    "distribuées", stylelabel)
    sheet.write_merge(27, 27, 0, 8, "")
    sheet.write_merge(28, 28, 0, 12, "", styleborformbutton)

    sheet.write_merge(2, 2, 1, 1,
                      report.entity.display_short_health_hierarchy(),
                      styleentity)
    sheet.write(3, 1, report.entity.slug, styletitle)

    sheet.write_merge(1, 1, 0, 12, "", styledescription)
    sheet.write(2, 2, "Mois", styledescription)
    sheet.write(2, 3, report.period.middle().month, styledate)
    sheet.write(2, 4, "", styledescription)
    sheet.write(2, 5, "Année", styledescription)
    sheet.write(2, 6, report.period.middle().year, styledate)
    sheet.write_merge(2, 2, 7, 12, "", styledescription)

    # SECTION Consultation
    sheet.write_merge(4, 4, 2, 7, "Consultation", styletitle)

    # les données de < 5 ans
    sheet.write_merge(5, 5, 2, 3, "< 5 ans", styletitle)
    sheet.write_merge(
        6, 6, 2, 3, report.u5_total_consultation_all_causes, stylevariable)
    sheet.write_merge(
        7, 7, 2, 3, report.u5_total_suspected_malaria_cases, stylevariable)
    sheet.write_merge(
        8, 8, 2, 3, report.u5_total_tested_malaria_cases, stylevariable)
    sheet.write_merge(
        9, 9, 2, 3, report.u5_total_confirmed_malaria_cases, stylevariable)
    sheet.write_merge(
        10, 10, 2, 3, report.u5_total_simple_malaria_cases, stylevariable)
    sheet.write_merge(
        11, 11, 2, 3, report.u5_total_severe_malaria_cases, stylevariable)
    sheet.write_merge(
        12, 12, 2, 3, report.u5_total_treated_malaria_cases, stylevariable)

    # les données de 5 ans et plus
    sheet.write_merge(5, 5, 4, 5, "5 ans et plus", styletitle)
    sheet.write_merge(
        6, 6, 4, 5, report.o5_total_consultation_all_causes, stylevariable)
    sheet.write_merge(
        7, 7, 4, 5, report.o5_total_suspected_malaria_cases, stylevariable)
    sheet.write_merge(
        8, 8, 4, 5, report.o5_total_tested_malaria_cases, stylevariable)
    sheet.write_merge(
        9, 9, 4, 5, report.o5_total_confirmed_malaria_cases, stylevariable)
    sheet.write_merge(
        10, 10, 4, 5, report.o5_total_simple_malaria_cases, stylevariable)
    sheet.write_merge(
        11, 11, 4, 5, report.o5_total_severe_malaria_cases, stylevariable)
    sheet.write_merge(
        12, 12, 4, 5, report.o5_total_treated_malaria_cases, stylevariable)

    # les données des Femmes enceintes
    sheet.write_merge(5, 5, 6, 7, "Femmes enceintes", styletitle)
    sheet.write_merge(
        6, 6, 6, 7, report.pw_total_consultation_all_causes, stylevariable)
    sheet.write_merge(
        7, 7, 6, 7, report.pw_total_suspected_malaria_cases, stylevariable)
    sheet.write_merge(
        8, 8, 6, 7, report.pw_total_tested_malaria_cases, stylevariable)
    sheet.write_merge(
        9, 9, 6, 7, report.pw_total_confirmed_malaria_cases, stylevariable)
    sheet.write_merge(
        10, 10, 6, 7, report.pw_total_simple_malaria_cases or 0,
        stylevariable)
    sheet.write_merge(
        11, 11, 6, 7, report.pw_total_severe_malaria_cases, stylevariable)
    sheet.write_merge(
        12, 12, 6, 7, report.pw_total_treated_malaria_cases, stylevariable)
    # SECTION Hospitalisations
    sheet.write_merge(14, 14, 2, 7, "Hospitalisations", styletitle)
    # les données de < 5 ans
    sheet.write_merge(15, 15, 2, 3, "< 5 ans", styletitle)
    sheet.write_merge(
        16, 16, 2, 3, report.u5_total_inpatient_all_causes, stylevariable)
    sheet.write_merge(
        17, 17, 2, 3, report.u5_total_malaria_inpatient, stylevariable)
    # + 5 ans
    sheet.write_merge(
        15, 15, 4, 5, " + 5 ans", styletitle)
    sheet.write_merge(
        16, 16, 4, 5, report.o5_total_inpatient_all_causes, stylevariable)
    sheet.write_merge(
        17, 17, 4, 5, report.o5_total_malaria_inpatient, stylevariable)

    # les données des Femmes enceintes
    sheet.write_merge(15, 15, 6, 7, "Femmes enceintes", styletitle)
    sheet.write_merge(
        16, 16, 6, 7, report.pw_total_inpatient_all_causes, stylevariable)
    sheet.write_merge(
        17, 17, 6, 7, report.pw_total_malaria_inpatient, stylevariable)

    # SECTION Decès
    sheet.write_merge(19, 19, 2, 7, "Decès", styletitle)

    # * les données de < 5 ans
    sheet.write_merge(20, 20, 2, 3, "< 5 ans", styletitle)
    sheet.write_merge(
        21, 21, 2, 3, report.u5_total_death_all_causes, stylevariable)
    sheet.write_merge(
        22, 22, 2, 3, report.u5_total_malaria_death, stylevariable)

    # les données de 5 ans et plus
    sheet.write_merge(20, 20, 4, 5, "5 ans et plus", styletitle)
    sheet.write_merge(
        21, 21, 4, 5, report.o5_total_death_all_causes, stylevariable)
    sheet.write_merge(
        22, 22, 4, 5, report.o5_total_malaria_death, stylevariable)

    # les données de Femmes enceintes
    sheet.write_merge(20, 20, 6, 7, "Femmes enceintes", styletitle)
    sheet.write_merge(
        21, 21, 6, 7, report.pw_total_death_all_causes, stylevariable)
    sheet.write_merge(
        22, 22, 6, 7, report.pw_total_malaria_death, stylevariable)

    # SECTION Moustiquaires imprégnéés d'insecticide distrivuées
    # < 5 ans
    sheet.write_merge(25, 25, 2, 3, "< 5 ans", styletitle)
    sheet.write_merge(
        26, 26, 2, 3, report.u5_total_distributed_bednets, stylevariable)
    sheet.write_merge(
        25, 25, 4, 5, "Femmes enceintes", styletitle)
    sheet.write_merge(
        26, 26, 4, 5, report.pw_total_distributed_bednets, stylevariable)

    # SECTION Rupture de stock CTA pendant le mois (Oui, Non)
    sheet.write_merge(3, 3, 9, 12, "Rupture de stock CTA pendant"
                                   "le mois", styletitle)
    sheet.write_merge(4, 4, 9, 11, "CTA Nourisson - Enfant", stylelabel)
    sheet.write(
        4, 12, report_status_verbose(
            report.stockout_act_children), stylevariable)
    sheet.write_merge(5, 5, 9, 11, "CTA Adolescent", stylelabel)
    sheet.write(
        5, 12, report_status_verbose(report.stockout_act_youth), stylevariable)
    sheet.write_merge(6, 6, 9, 11, "CTA Adulte", stylelabel)
    sheet.write(
        6, 12, report_status_verbose(report.stockout_act_adult), stylevariable)
    sheet.write_merge(7, 7, 8, 12, "")

    # SECTION PEC de cas de Paludisme grave Rupture de soctk OUI/NON
    sheet.write_merge(8, 8, 9, 12, "PEC de cas de Paludisme grave", styletitle)
    sheet.write_merge(9, 9, 9, 12, "Rupture de soctk OUI/NON", styletitle)
    sheet.write_merge(10, 10, 9, 11, "Arthemether injectable", stylelabel)
    sheet.write(
        10, 12, report_status_verbose(
            report.stockout_artemether), stylevariable)
    sheet.write_merge(11, 11, 9, 11, "Quinine Injectable", stylelabel)
    sheet.write(
        11, 12, report_status_verbose(report.stockout_quinine), stylevariable)
    sheet.write_merge(12, 12, 9, 11, "Serum", stylelabel)
    sheet.write(
        12, 12, report_status_verbose(report.stockout_serum), stylevariable)

    # SECTION Rupture de stock pendant le mois O/N (Oui, Non)
    sheet.write_merge(
        14, 14, 10, 12, "Rupture de stock pendant le mois O/N", styletitle)
    sheet.write_merge(15, 15, 10, 11, "MILD", stylelabel)
    sheet.write(
        15, 12, report_status_verbose(report.stockout_bednet), stylevariable)
    sheet.write_merge(16, 16, 10, 11, "TDR", stylelabel)
    sheet.write(
        16, 12, report_status_verbose(report.stockout_rdt), stylevariable)
    sheet.write_merge(17, 17, 10, 11, "SP", stylelabel)
    sheet.write(
        17, 12, report_status_verbose(report.stockout_sp), stylevariable)

    # SECTION CPN/SP des femme s enceintes (nbre)
    sheet.write_merge(
        19, 20, 10, 12, "CPN/SP des femmes enceintes (nbre)", styletitleform)
    sheet.write_merge(21, 21, 10, 11, "CPN 1", stylelabel)
    sheet.write(21, 12, report.pw_total_anc1, stylevariable)
    sheet.write_merge(22, 22, 10, 11, "SP 1", stylelabel)
    sheet.write(22, 12, report.pw_total_sp1, stylevariable)
    sheet.write_merge(23, 23, 10, 11, "SP 2 et +", stylelabel)
    sheet.write(23, 12, report.pw_total_sp2, stylevariable)

    sheet.write(25, 9, "Nom et Prénom : {}".format(report.created_by.name()))
    sheet.write(26, 9, "Le Responsable CSCom/CSRéf")
    sheet.write(27, 9, "Date :")
    sheet.write(27, 10, report.created_on.day, styledate)
    sheet.write(27, 11, report.created_on.month, styledate)
    sheet.write(27, 12, report.created_on.year, styledate)

    sheet.write_merge(0, 28, 13, 13, "", styleborformright)

    if report.validated_on:
        validation_str = "Validé le {on} par {by}".format(
            on=text_type(report.validated_on.strftime("%c").decode('utf8')),
            by=text_type(report.validated_by))
        if report.auto_validated:
            validation_str = "{} (auto)".format(validation_str)
        sheet.write(31, 0, validation_str)
    else:
        sheet.write(31, 0, report.verbose_validation_status)
    sheet.write(32, 0, report.verbose_arrival_status)

    # if report.REPORTING_LEVEL == AGGREGATED_LEVEL:
    if is_aggregated(report):
        sheet.write(35, 0, "Sources Primaires", styletitle)
        i = 36
        for source in report.indiv_sources.all():
            source_str = "%(entity)s - %(receipt)s" \
                         % {'entity': source.entity.display_name(),
                            'receipt': report.receipt}
            sheet.write(i, 0, source_str, stylelabel)
            i += 1

        sheet.write(i, 0, "Sources Agrégées", styletitle)
        i += 1
        for source in report.agg_sources.all():
            source_str = "%(entity)s - %(receipt)s" \
                         % {'entity': source.entity.display_name(),
                            'receipt': report.receipt}
            sheet.write(i, 0, source_str, stylelabel)
            i += 1

    stream = StringIO.StringIO()
    book.save(stream)

    return stream


def malaria_weekly_routine_weeklong_as_xls(report):

    template_path = os.path.join(
        get_domain().module_path,
        'fixtures', 'template-malaria-weekly-routine-weeklong.xls')
    template = open_workbook(template_path, formatting_info=True)
    copy_week_book = copy(template)
    sh_report = copy_week_book.get_sheet(0)
    del(template)

    xls_update_value_only(
        sh_report, 1, 2, report.entity.display_short_health_hierarchy())
    xls_update_value_only(sh_report, 1, 3, report.entity.slug)

    xls_update_value_only(sh_report, 4, 3, report.created_by.name())
    xls_update_value_only(sh_report, 4, 2, report.period.casted().strid())

    col = 2
    row = 6

    xls_update_value_only(
        sh_report, col, row + 1, report.day1_u5_total_confirmed_malaria_cases)
    xls_update_value_only(
        sh_report, col, row + 2, report.day1_o5_total_confirmed_malaria_cases)
    xls_update_value_only(
        sh_report, col, row + 3, report.day1_pw_total_confirmed_malaria_cases)
    col += 1
    xls_update_value_only(
        sh_report, col, row + 1, report.day2_u5_total_confirmed_malaria_cases)
    xls_update_value_only(
        sh_report, col, row + 2, report.day2_o5_total_confirmed_malaria_cases)
    xls_update_value_only(
        sh_report, col, row + 3, report.day2_pw_total_confirmed_malaria_cases)
    col += 1
    xls_update_value_only(
        sh_report, col, row + 1, report.day3_u5_total_confirmed_malaria_cases)
    xls_update_value_only(
        sh_report, col, row + 2, report.day3_o5_total_confirmed_malaria_cases)
    xls_update_value_only(
        sh_report, col, row + 3, report.day3_pw_total_confirmed_malaria_cases)
    col += 1
    xls_update_value_only(
        sh_report, col, row + 1, report.day4_u5_total_confirmed_malaria_cases)
    xls_update_value_only(
        sh_report, col, row + 2, report.day4_o5_total_confirmed_malaria_cases)
    xls_update_value_only(
        sh_report, col, row + 3, report.day4_pw_total_confirmed_malaria_cases)
    col += 1
    xls_update_value_only(
        sh_report, col, row + 1, report.day5_u5_total_confirmed_malaria_cases)
    xls_update_value_only(
        sh_report, col, row + 2, report.day5_o5_total_confirmed_malaria_cases)
    xls_update_value_only(
        sh_report, col, row + 3, report.day5_pw_total_confirmed_malaria_cases)
    col += 1
    xls_update_value_only(
        sh_report, col, row + 1, report.day6_u5_total_confirmed_malaria_cases)
    xls_update_value_only(
        sh_report, col, row + 2, report.day6_o5_total_confirmed_malaria_cases)
    xls_update_value_only(
        sh_report, col, row + 3, report.day6_pw_total_confirmed_malaria_cases)
    col += 1
    xls_update_value_only(
        sh_report, col, row + 1, report.day7_u5_total_confirmed_malaria_cases)
    xls_update_value_only(
        sh_report, col, row + 2, report.day7_o5_total_confirmed_malaria_cases)
    xls_update_value_only(
        sh_report, col, row + 3, report.day7_pw_total_confirmed_malaria_cases)
    col += 1
    xls_update_value_only(
        sh_report, col, row + 1, report.u5_total_confirmed_malaria_cases)
    xls_update_value_only(
        sh_report, col, row + 2, report.o5_total_confirmed_malaria_cases)
    xls_update_value_only(
        sh_report, col, row + 3, report.pw_total_confirmed_malaria_cases)

    for col, coly in enumerate(["C", "D", "E", "F", "G", "H", "I"]):
        xls_update_value_only(sh_report, col + 2, row + 4,
                              xlwt.Formula("SUM({}8:{}10)".format(coly, coly)))

    xls_update_value_only(
        sh_report, col + 3, row + 4, xlwt.Formula("SUM(J8:J10)"))

    stream = StringIO.StringIO()
    copy_week_book.save(stream)

    return stream


def malaria_weekly_routine_as_xls(report):

    template_path = os.path.join(
        get_domain().module_path,
        'fixtures', 'template-malaria-weekly.xls')
    template = open_workbook(template_path, formatting_info=True)
    copy_week_book = copy(template)
    sh_report = copy_week_book.get_sheet(0)
    del(template)

    xls_update_value_only(
        sh_report, 1, 2, report.entity.display_short_health_hierarchy())
    xls_update_value_only(sh_report, 1, 3, report.entity.slug)
    xls_update_value_only(sh_report, 3, 2, report.period.casted().strid())
    xls_update_value_only(sh_report, 3, 3, report.created_by.name())

    col = 2
    row = 5

    xls_update_value_only(
        sh_report, col, row + 1, report.u5_total_confirmed_malaria_cases)
    xls_update_value_only(
        sh_report, col, row + 2, report.o5_total_confirmed_malaria_cases)
    xls_update_value_only(
        sh_report, col, row + 3, report.pw_total_confirmed_malaria_cases)
    xls_update_value_only(sh_report, col, row + 4, xlwt.Formula("SUM(C7:C9)"))

    stream = StringIO.StringIO()
    copy_week_book.save(stream)

    return stream


def all_malariar_as_xls(save_to=None):

    from snisi_malaria.models import MalariaR

    reports = MalariaR.objects.all() \
                      .order_by('created_on',
                                'entity__parent__parent__parent__name',
                                'entity__parent__parent__name',
                                'entity__name')

    wb = xlwt.Workbook()
    sheet = wb.add_sheet("malaria-routine-reports")

    headers = ["CODE", "REGION", "DISTRICT", "CSCOM",
               "YEAR", "MONTH", "RECEIVED_ON", "VALIDATED_ON", "AUTO_VALIDATED"] + MalariaR.data_fields()

    for col, item in enumerate(headers):
        sheet.write(0, col, item)

    row = 1
    for report in reports.iterator():
        col = 0
        sheet.write(row, col, report.entity.slug)
        col += 1
        sheet.write(row, col, report.entity.get_health_region().display_name())
        col += 1
        sheet.write(
            row, col, report.entity.get_health_district().display_name())
        col += 1
        sheet.write(row, col, report.entity.display_name())
        col += 1
        sheet.write(row, col, report.period.middle().year)
        col += 1
        sheet.write(row, col, report.period.middle().month)
        col += 1
        sheet.write(row, col, getattr(report.created_on, 'isoformat', lambda: "")())
        col += 1
        sheet.write(row, col, getattr(report.validated_on, 'isoformat', lambda: "")())
        col += 1
        sheet.write(row, col, report.auto_validated)
        col += 1
        for field in report.data_fields():
            sheet.write(row, col, report.get(field))
            col += 1
        row += 1

    if save_to:
        wb.save(save_to)
        return

    stream = StringIO.StringIO()
    wb.save(stream)

    return stream


def all_dailymalariar_xls(save_to=None):

    from snisi_malaria.models import DailyMalariaR

    reports = DailyMalariaR.objects.all() \
        .order_by('period__start_on',
                  'entity__parent__parent__parent__name',
                  'entity__parent__parent__name',
                  'entity__name')

    wb = xlwt.Workbook()
    sheet = wb.add_sheet("malaria-daily-routine-reports")

    headers = ["CODE", "REGION", "DISTRICT", "CSCOM", "YEAR", "MONTH", "DAY",
               "RECEIVED_ON"] + DailyMalariaR.data_fields()

    for col, item in enumerate(headers):
        sheet.write(0, col, item)

    row = 1
    for report in reports.iterator():

        col = 0
        sheet.write(row, col, report.entity.slug)
        col += 1
        sheet.write(row, col, report.entity.get_health_region().display_name())
        col += 1
        sheet.write(
            row, col, report.entity.get_health_district().display_name())
        col += 1
        sheet.write(row, col, report.entity.display_name())
        col += 1
        sheet.write(row, col, report.period.middle().year)
        col += 1
        sheet.write(row, col, report.period.middle().month)
        col += 1
        sheet.write(row, col, report.period.middle().day)
        col += 1
        sheet.write(row, col, getattr(report.created_on, 'isoformat', lambda: "")())
        col += 1

        for field in report.data_fields():
            sheet.write(row, col, report.get(field))
            col += 1

        row += 1

    if save_to:
        wb.save(save_to)
        return

    stream = StringIO.StringIO()
    wb.save(stream)

    return stream
