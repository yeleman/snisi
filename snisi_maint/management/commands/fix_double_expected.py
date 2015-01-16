#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim: ai ts=4 sts=4 et sw=4 nu

from __future__ import (unicode_literals, absolute_import,
                        division, print_function)
import logging

from django.core.management.base import BaseCommand
from django.utils import timezone

from snisi_core.models.Reporting import ExpectedReporting

logger = logging.getLogger(__name__)


class Command(BaseCommand):

    def handle(self, *args, **options):

        now = timezone.now()

        for exp in ExpectedReporting.objects.filter(
                reporting_period__end_on__gte=now,
                completion_status=u''):

            logger.info(exp)

            params = {
                'report_class': exp.report_class,
                'reporting_role': exp.reporting_role,

                'period': exp.period,
                'within_period': exp.within_period,

                'entity': exp.entity,
                'within_entity': exp.within_entity,

                'reporting_period': exp.reporting_period,
                'extended_reporting_period': exp.extended_reporting_period,

                'amount_expected': exp.amount_expected,

                'completion_status': ExpectedReporting.COMPLETION_MISSING,
            }

            if not ExpectedReporting.objects.filter(**params).count():
                # no duplicates on this one.
                logger.info("... No duplicate")
                continue

            good = ExpectedReporting.objects.filter(**params).get()

            if not exp.satisfied and not exp.arrived_reports.count():
                logger.info(". DELETETIN exp: {}".format(exp))
                exp.delete()
            else:
                logger.info("CAN'T DELETE EXP as satisfied: {}".format(exp))
                logger.info(good)
