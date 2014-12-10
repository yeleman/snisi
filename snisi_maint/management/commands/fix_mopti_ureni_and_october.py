#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim: ai ts=4 sts=4 et sw=4 nu

from __future__ import (unicode_literals, absolute_import,
                        division, print_function)
import logging

from django.core.management.base import BaseCommand

from snisi_core.models.Periods import MonthPeriod
from snisi_core.models.Entities import Entity
from snisi_core.models.Reporting import (ExpectedReporting, ReportClass)

logger = logging.getLogger(__name__)


class Command(BaseCommand):

    def handle(self, *args, **options):

        october = MonthPeriod.from_url_str("10-2014")
        november = MonthPeriod.from_url_str("11-2014")
        mopti_csref = Entity.get_or_none("J5C6")

        logger.info("Remove Expected and data for {}".format(october))

        rc_slugs = ['nutrition_monthly_routine',
                    'nutrition_monthly_routine_aggregated',
                    'nut_urenam_monthly_routine',
                    'nut_urenam_monthly_routine_aggregated',
                    'nut_urenas_monthly_routine',
                    'nut_urenas_monthly_routine_aggregated',
                    'nut_ureni_monthly_routine',
                    'nut_ureni_monthly_routine_aggregated',
                    'nut_stocks_monthly_routine',
                    'nut_stocks_monthly_routine_aggregated',
                    'nutrition_weekly_routine',
                    'nutrition_weekly_routine_aggregated']

        for rc_slug in rc_slugs:
            rc = ReportClass.get_or_none(rc_slug)

            logger.info("Deleting expecteds")
            ExpectedReporting.objects.filter(
                report_class=rc,
                period__end_on__lte=october.end_on).delete()

            logger.info("Deleting reports and expected validations")
            rqs = rc.report_class.objects.filter(
                period__end_on__lte=october.end_on)
            for r in rqs:
                logger.info("\treport: {}".format(r))
                if r.expected_reportings.count():
                    logger.info("\tfound exp")
                    r.expected_reportings.all().delete()
                if r.expected_validations.count():
                    logger.info("\tfound expval")
                    r.expected_validations.all().delete()
                logger.info("\tdeleting report.")
                r.delete()

        logger.info("Updating Mopti CSRef")
        mopti_csref.has_urenam = False
        mopti_csref.has_urenas = False
        mopti_csref.save()

        logger.info("Removing Mopti CSRef Expected")
        ExpectedReporting.objects.filter(
            entity__slug=mopti_csref.slug,
            report_class__slug__in=['nut_urenam_monthly_routine',
                                    'nut_urenam_monthly_routine_aggregated',
                                    'nut_urenas_monthly_routine',
                                    'nut_urenas_monthly_routine_aggregated'],
            period=november).delete()

        logger.info("done.")
