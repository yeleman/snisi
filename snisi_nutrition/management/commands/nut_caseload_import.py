#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim: ai ts=4 sts=4 et sw=4 nu

from __future__ import (unicode_literals, absolute_import,
                        division, print_function)
import logging

import xlrd
from django.core.management.base import BaseCommand
from optparse import make_option

from snisi_nutrition.models.Caseload import ExpectedCaseload

logger = logging.getLogger(__name__)


def import_expected_caseload_from_xls(year, filepath):

    try:
        book = xlrd.open_workbook(filepath)
        ws = book.sheet_by_index(0)
    except Exception as e:
        logger.warning("Unable to read Excel file {path}. "
                       "Raised {e}".format(path=filepath, e=e))
        return

    columns = ['region_name', 'district_name', 'entity_slug',
               'u59o6_sam', 'u59_sam', 'u59o6_mam', 'u59_mam', 'pw_mam',
               'u59o6_sam_80pc', 'u59_sam_80pc',
               'u59o6_mam_80pc', 'u59_mam_80pc', 'pw_mam_80pc']

    def data_for(row_num):
        return {
            field: ws.row_values(row_num)[col_num]
            for col_num, field in enumerate(columns)
        }

    for row_num in range(2, ws.nrows):
        entry = data_for(row_num)
        if not entry['region_name']:
            continue

        if not entry['u59o6_sam']:
            logger.warning(
                "Skipping {region_name}/{district_name}/{entity_slug}"
                .format(**entry))
            continue

        # make sure slug is string
        if isinstance(entry['entity_slug'], (float, int)):
            entry['entity_slug'] = str(int(entry['entity_slug']))

        for field in ExpectedCaseload.DATA_FIELDS:
            try:
                int(entry[field])
            except:
                logger.debug(entry)
                logger.error("Invalid data for {f} at {e}"
                             .format(f=field, e=entry['district_name']))
                return

        try:
            exp = ExpectedCaseload.update_or_create(year=year, **entry)
            assert exp is not None
        except Exception as e:
            logger.debug(entry)
            logger.error("Unable to save caseload")
            logger.exception(e)
            return
        finally:
            logger.info("Created/updated {}".format(exp.entity.casted()))

    return True


class Command(BaseCommand):

    option_list = BaseCommand.option_list + (
        make_option('-x',
                    help='Excel file',
                    action='store',
                    dest='filename'),
        make_option('-y',
                    help='year',
                    action='store',
                    dest='year'),
    )

    def handle(self, *args, **options):

        try:
            year = int(options.get('year'))
            assert year > 2013 and year < 2025
        except:
            logger.error("Value for year ({}) is incorect"
                         .format(options.get('year')))
            return

        filepath = options.get('filename')
        try:
            input_xls_file = open(filepath, 'r')
            input_xls_file.close()
        except:
            logger.error("Unable to open XLS file ({})".format(filepath))
            return

        logger.info("Importing Expected Caseload for {}".format(year))

        if import_expected_caseload_from_xls(year=year, filepath=filepath):
            logger.info("Successfuly imported caseload!")
        else:
            logger.error("Unable to import caseload data. Check trace.")
