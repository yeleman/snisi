#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim: ai ts=4 sts=4 et sw=4 nu

from __future__ import (unicode_literals, absolute_import,
                        division, print_function)
import logging

from django.core.management.base import BaseCommand

from snisi_core.models.Projects import Cluster
from snisi_core.models.Periods import MonthPeriod
from snisi_core.models.Reporting import ExpectedReporting


logger = logging.getLogger(__name__)


class Command(BaseCommand):

    def handle(self, *args, **options):

        cluster = Cluster.get_or_none("malaria_monthly_routine")
        periods = MonthPeriod.all_from(MonthPeriod.from_url_str("06-2011"))

        for period in periods:
            logger.info(period)

            for entity in cluster.members():
                qs = ExpectedReporting.objects.filter(
                    entity=entity, period=period,
                    report_class__slug="malaria_monthly_routine")

                if qs.count() == 2:
                    logger.info("Removing {}".format(qs[1]))
                    qs[1].delete()
