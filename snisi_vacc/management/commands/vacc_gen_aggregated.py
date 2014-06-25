#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim: ai ts=4 sts=4 et sw=4 nu

from __future__ import (unicode_literals, absolute_import,
                        division, print_function)
import logging
import datetime

from django.core.management.base import BaseCommand

from snisi_core.models.Periods import MonthPeriod
from snisi_core.models.Projects import Cluster
from snisi_vacc.expected import create_expected_for
from snisi_vacc.aggregations import (generate_district_reports,
                                     generate_region_country_reports)
from snisi_tools.datetime import DEBUG_change_system_date

logger = logging.getLogger(__name__)

speriod = MonthPeriod.from_url_str("01-2013")
eperiod = MonthPeriod.from_url_str("12-2013")
periods = MonthPeriod.all_from(speriod, eperiod)


class Command(BaseCommand):

    def handle(self, *args, **options):

        coverage_cluster = Cluster.objects.get(slug="vacc_coverage_routine")

        should_switch = not coverage_cluster.is_active

        if should_switch:
            coverage_cluster.is_active = True
            coverage_cluster.save()

        for period in periods:
            logger.info(period)
            district_date = period.following().start_on + datetime.timedelta(days=10)
            DEBUG_change_system_date(district_date, True)

            generate_district_reports(period)
            generate_region_country_reports(period)

        if should_switch:
            coverage_cluster.is_active = False
            coverage_cluster.save()

        DEBUG_change_system_date(None, True)
