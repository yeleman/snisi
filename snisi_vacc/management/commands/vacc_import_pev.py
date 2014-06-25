#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim: ai ts=4 sts=4 et sw=4 nu

from __future__ import (unicode_literals, absolute_import,
                        division, print_function)
import logging
import os
import datetime
from optparse import make_option

from django.core.management.base import BaseCommand
from django.utils import timezone
from xlrd import open_workbook

from snisi_core.models.Periods import MonthPeriod
from snisi_core.models.Entities import Entity
from snisi_core.models.Providers import Provider
from snisi_vacc import PROJECT_BRAND
from snisi_vacc.integrity import create_pev_report, VaccCovRIntegrityChecker
from snisi_tools.datetime import DEBUG_change_system_date

logger = logging.getLogger(__name__)


districts = {
    "TY60": "MACINA",
    "8R92": "MARKALA",
    "YF98": "SEGOU_VF",
    "KZF8": "SAN",
    "84C0": "TOMINIAN",
    "A6T3": "BLA",
    "X952": "NIONO",
    "XN90": "BAROUELI",
}

sheets = {
    'CV1': 2,
    'CV2': 3,
    'AB1': 4
}

vaccin_matrix = {
    'bcg': ('CV1', 5, 6),
    'penta3': ('CV1', 70, 6),
    'measles': ('CV2', 5, 6),
    'abandonment': ('AB1', 17, 5),
}

speriod = MonthPeriod.from_url_str("01-2013")
eperiod = MonthPeriod.from_url_str("12-2013")
periods = MonthPeriod.all_from(speriod, eperiod)

def cl_slug(slug):
    return unicode(slug).strip().upper()[1:]


def cl_value(value):
    return float(value) if len(unicode(value).strip()) else None


def get_entities_values_for(wb, vaccin, period):
    """ dict of slug: value for vaccin at given period """

    sheet_name, col_start, row_start = vaccin_matrix.get(vaccin)
    sheet = wb.sheet_by_name(wb.sheet_names()[sheets.get(sheet_name)])

    col = periods.index(period) + col_start

    return {cl_slug(sheet.cell_value(row, 0)): cl_value(sheet.cell_value(row, col))
            for row in range(row_start, row_start + 42) if cl_slug(sheet.cell_value(row, 0))}


class Command(BaseCommand):

    option_list = BaseCommand.option_list + (
        make_option('-p',
                    help='Path to PEV folder',
                    action='store',
                    dest='folder'),
    )

    def handle(self, *args, **options):

        autobot = Provider.get_or_none('autobot')

        if not options.get('folder', None) or not os.path.exists(options.get('folder')):
            logger.error("Unable to access data folder {}".format(options.get('folder')))
            return

        for district in districts.values():

            fname = os.path.join(options.get('folder'),
                                 'PEV_2013_{}.xlsx'.format(district))
            wb = open_workbook(fname)

            logger.info(district)

            for period in periods:

                logger.info(period)

                bcg_data = get_entities_values_for(wb, 'bcg', period)
                penta3_data = get_entities_values_for(wb, 'penta3', period)
                measles_data = get_entities_values_for(wb, 'measles', period)
                abandonment_data = get_entities_values_for(wb, 'abandonment', period)

                slug_data = {}
                for slug, bcg in bcg_data.items():
                    slug_data.update({slug: {'bcg': bcg,
                                             'penta3': penta3_data.get(slug),
                                             'measles': measles_data.get(slug),
                                             'abandonment': abandonment_data.get(slug),
                                             'entity': Entity.get_or_none(slug)
                                             }
                                    })

                for data in slug_data.values():

                    if None in data.values():
                        continue

                    completed_on = period.start_on + datetime.timedelta(days=2)
                    DEBUG_change_system_date(period.following().start_on + datetime.timedelta(days=2), True)

                    entity = data['entity']

                    checker = VaccCovRIntegrityChecker()

                    checker.set('submit_time', timezone.now())
                    checker.set('hc', entity.slug)
                    checker.set('submitter', autobot)
                    checker.set('year', period.middle().year)
                    checker.set('month', period.middle().month)

                    checker.set('bcg_coverage', data.get('bcg'))
                    checker.set('polio3_coverage', data.get('penta3'))
                    checker.set('measles_coverage', data.get('measles'))
                    checker.set('polio3_abandonment_rate', data.get('abandonment'))

                    checker.check()

                    if not checker.is_valid():
                        logger.error(checker.errors.pop().render(short=True))
                        continue
                        # DEBUG_change_system_date(None, True)
                        # return

                    create_pev_report(
                        provider=autobot,
                        expected_reporting=checker.get('expected_reporting'),
                        completed_on=completed_on,
                        integrity_checker=checker,
                        data_source=fname)

            DEBUG_change_system_date(None, True)

            del(wb)
