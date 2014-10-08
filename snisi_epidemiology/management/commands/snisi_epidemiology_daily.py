#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim: ai ts=4 sts=4 et sw=4 nu

from __future__ import (unicode_literals, absolute_import,
                        division, print_function)
import logging
import datetime

from django.core.management.base import BaseCommand
from django.utils import timezone

from snisi_epidemiology import (ROUTINE_REPORTING_END_WEEKDAY,
                                ROUTINE_DISTRICT_AGG_DAYS_DELTA,
                                ROUTINE_REGION_AGG_DAYS_DELTA)
from snisi_epidemiology.models import EpiWeekPeriod
from snisi_core.models.PeriodicTasks import PeriodicTask
from snisi_epidemiology.aggregations import (generate_district_reports,
                                             generate_region_country_reports)

logger = logging.getLogger(__name__)


class Command(BaseCommand):

    def handle(self, *args, **options):

        logger.info("snisi_epidemiology daily-checkups")

        now = timezone.now()

        category_matrix = {
            'end_of_district_period': generate_district_reports,
            'end_of_region_period': generate_region_country_reports,
        }

        def handle_category(category, period):
            slug = "{period}_{category}".format(period=period.strid(),
                                                category=category)
            task, created = PeriodicTask.get_or_create(slug, category)

            if task.can_trigger():
                category_matrix.get(category)(period)
                task.trigger()

        # number and position of weeks across month is inconsistent.
        # loop through potential past weeks and process if possible
        periods = []
        period = EpiWeekPeriod.current()
        while period.end_on < now:
            periods.append(period)

        for period in periods:
            reporting_end = period.end_on + datetime.timedelta(
                days=ROUTINE_REPORTING_END_WEEKDAY)

            # validate all HC reports
            # create aggregated for district
            # create expected-validation for district
            # send notification to regions
            if reporting_end + datetime.timedelta(
                    days=ROUTINE_DISTRICT_AGG_DAYS_DELTA) < now:
                handle_category("end_of_district_period")

            # validate all district reports
            # create aggregated for region
            # create aggregated for country
            # send notification to central/national
            if reporting_end + datetime.timedelta(
                    days=ROUTINE_REGION_AGG_DAYS_DELTA) < now:
                handle_category("end_of_region_period")
