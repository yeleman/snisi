#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim: ai ts=4 sts=4 et sw=4 nu

from __future__ import (unicode_literals, absolute_import,
                        division, print_function)
import logging
import os
import datetime

from django.core.management.base import BaseCommand
from optparse import make_option

from snisi_core.models.Providers import Provider
from snisi_core.models.Entities import Entity
from snisi_core.models.Projects import Cluster, Participation
from snisi_core.models.FixedWeekPeriods import (FixedMonthFirstWeek,
                                                FixedMonthSecondWeek,
                                                FixedMonthThirdWeek,
                                                FixedMonthFourthWeek,
                                                FixedMonthFifthWeek)
from snisi_malaria.xls_import import EpidemioMalariaRForm
from snisi_tools.datetime import DEBUG_change_system_date

logger = logging.getLogger(__name__)


class Command(BaseCommand):

    option_list = BaseCommand.option_list + (
        make_option('-p',
                    help='Path (folder) from which to import xls files',
                    action='store',
                    default='./',
                    dest='xls_root'),
        make_option('-u',
                    help='Username of the Provider to submit data from',
                    action='store',
                    dest='username'),
    )


    def handle(self, *args, **options):

        cluster = Cluster.get_or_none("malaria_weekly_epidemiology")
        if not len(cluster.members()):
            logger.info("Creating participations")
            for entity_slug in ("ACE3", "3ZF3"):
                entity = Entity.get_or_none(entity_slug)
                Participation.objects.create(cluster=cluster, entity=entity)


        provider = Provider.get_or_none(options.get('username'))
        if provider is None:
            logger.error("Provided username does not match a provider.")
            return

        xls_root = options.get('xls_root')
        if not os.path.exists(xls_root):
            logger.error("Provided path does not exist.")
            return

        logger.info("Starting import from {}".format(xls_root))

        seconds = 12*60*60

        for filename in sorted(os.listdir(xls_root)):
            if not filename.endswith('.xls'):
                continue

            filepath = os.path.join(xls_root, filename)
            logger.debug("Opening {}".format(filepath))

            # Z3ZF3-S1-1-2013
            slug, week, month, year = filename.split('.xls')[0].split('-')
            week = int(week[1])
            month = int(month)
            year = int(year)

            period_classes = {
                1: FixedMonthFirstWeek,
                2: FixedMonthSecondWeek,
                3: FixedMonthThirdWeek,
                4: FixedMonthFourthWeek,
                5: FixedMonthFifthWeek,
            }

            periodcls = period_classes.get(week)
            period = periodcls.find_create_from(year=year, month=month)
            reporting_date = period.end_on + datetime.timedelta(days=1, seconds=seconds)

            DEBUG_change_system_date(reporting_date)

            logger.debug(reporting_date)


            excel_form = EpidemioMalariaRForm(filepath)
            excel_form.set('submit_time', reporting_date)
            excel_form.set('submitter', provider)
            excel_form.check()
            if excel_form.is_valid():
                report, text_message = excel_form.create_report(provider=provider)
                if report:
                    logger.info(text_message)
                    continue
            else:
                report = None
                logger.error("Unable to save report to DB")
                logger.error("ERR: {} - {}".format(filename, excel_form.errors.pop().render()))

        logger.info("All done.")
