#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim: ai ts=4 sts=4 et sw=4 nu

from __future__ import (unicode_literals, absolute_import,
                        division, print_function)
import logging

from django.core.management.base import BaseCommand

from snisi_core.models.Periods import MonthPeriod
from snisi_core.models.Reporting import (PERIODICAL_AGGREGATED,
                                         ExpectedValidation)

logger = logging.getLogger(__name__)


class Command(BaseCommand):

    def handle(self, *args, **options):

        logger.info("Issue. Region Validation Period withing period")

        for e in ExpectedValidation.objects.filter(satisfied=False):
            if e.validation_period.end_on < e.report.period.end_on and \
                    e.report.casted().REPORTING_TYPE == PERIODICAL_AGGREGATED:
                logger.info(e)
                e.validation_period = e.validation_period.following()
                e.save()

        logger.info("done.")
