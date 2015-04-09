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
from snisi_epidemiology import get_domain

logger = logging.getLogger(__name__)


def epid_activities_as_xls(report):
    """ Export les données d'un rapport epidemiologique en xls """

    template_path = os.path.join(get_domain().module_path,
                                 'fixtures', 'template-hebdo-MADO.xls')
    template = open_workbook(template_path, formatting_info=True)
    copy_week_book = copy(template)
    sh_report = copy_week_book.get_sheet(0)
    del(template)

    xls_update_value_only(sh_report,
                          4, 1, report.entity.display_short_health_hierarchy())
    xls_update_value_only(sh_report,
                          2, 1, report.entity.slug)
    xls_update_value_only(sh_report,
                          2, 2, report.period.middle().day)
    xls_update_value_only(sh_report,
                          4, 2, report.period.middle().month)
    xls_update_value_only(sh_report,
                          6, 2, report.period.middle().year)
    col = 1
    row = 5
    xls_update_value_only(sh_report,
                          col, row + 1, report.ebola_case)
    xls_update_value_only(sh_report,
                          col, row + 2, report.acute_flaccid_paralysis_case)
    xls_update_value_only(sh_report,
                          col, row + 3, report.influenza_a_h1n1_case)
    xls_update_value_only(sh_report,
                          col, row + 4, report.cholera_case)
    xls_update_value_only(sh_report,
                          col, row + 5, report.red_diarrhea_case)
    xls_update_value_only(sh_report,
                          col, row + 6, report.measles_case)
    xls_update_value_only(sh_report,
                          col, row + 7, report.yellow_fever_case)
    xls_update_value_only(sh_report,
                          col, row + 8, report.neonatal_tetanus_case)
    xls_update_value_only(sh_report,
                          col, row + 9, report.meningitis_case)
    xls_update_value_only(sh_report,
                          col, row + 10, report.rabies_case)
    xls_update_value_only(sh_report,
                          col, row + 11, report.acute_measles_diarrhea_case)
    xls_update_value_only(sh_report,
                          col, row + 12, report.other_notifiable_disease_case)
    col = 2
    row = 5
    xls_update_value_only(sh_report,
                          col, row + 1, report.ebola_death)
    xls_update_value_only(sh_report,
                          col, row + 2, report.acute_flaccid_paralysis_death)
    xls_update_value_only(sh_report,
                          col, row + 3, report.influenza_a_h1n1_death)
    xls_update_value_only(sh_report,
                          col, row + 4, report.cholera_death)
    xls_update_value_only(sh_report,
                          col, row + 5, report.red_diarrhea_death)
    xls_update_value_only(sh_report,
                          col, row + 6, report.measles_death)
    xls_update_value_only(sh_report,
                          col, row + 7, report.yellow_fever_death)
    xls_update_value_only(sh_report,
                          col, row + 8, report.neonatal_tetanus_death)
    xls_update_value_only(sh_report,
                          col, row + 9, report.meningitis_death)
    xls_update_value_only(sh_report,
                          col, row + 10, report.rabies_death)
    xls_update_value_only(sh_report,
                          col, row + 11, report.acute_measles_diarrhea_death)
    xls_update_value_only(sh_report,
                          col, row + 12, report.other_notifiable_disease_death)

    stream = StringIO.StringIO()
    copy_week_book.save(stream)

    return stream
