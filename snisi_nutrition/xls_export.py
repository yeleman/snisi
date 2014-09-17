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

logger = logging.getLogger(__name__)


def pfa_activities_as_xls(report):
    """ Export les données d'un rapport en xls """

    template_path = os.path.join(get_domain().module_path,
                                 'fixtures', 'template-nutrition.xls')

    template = open_workbook(template_path, formatting_info=True)
    copy_week_b = copy(template)
    sheet = copy_week_b.get_sheet(0)
    sheet.portrait = False
    del(template)

    xls_update_value_only(sheet, 4, 1,  report.entity.name)
    xls_update_value_only(sheet, 2, 1,  report.entity.slug)
    xls_update_value_only(sheet, 2, 2,  report.period.middle().month)
    xls_update_value_only(sheet, 4, 2,  report.period.middle().year)

    stream = StringIO.StringIO()
    copy_week_b.save(stream)

    return stream
