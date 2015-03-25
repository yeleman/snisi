#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim: ai ts=4 sts=4 et sw=4 nu

from __future__ import (unicode_literals, absolute_import,
                        division, print_function)
import logging
import datetime

from django.core.management.base import BaseCommand
from django.utils import timezone

from snisi_core.models.Periods import MonthPeriod
from snisi_core.models.PeriodicTasks import PeriodicTask
from snisi_nutrition import (DOMAIN_SLUG,
                             ROUTINE_DISTRICT_AGG_DAYS_DELTA,
                             ROUTINE_REGION_AGG_DAYS_DELTA,
                             ROUTINE_REPORTING_END_DAY,
                             ROUTINE_EXTENDED_REPORTING_END_DAY,
                             ROUTINE_DISTRICT_AGG_DAY,
                             ROUTINE_REGION_AGG_DAY)
from snisi_nutrition.models.Weekly import NutWeekPeriod
from snisi_nutrition.notifications import (
    end_of_reporting_period_notifications,
    end_of_extended_reporting_period_notifications,
    performance_indicators_notifications,
    inputs_stockouts_notifications)
from snisi_nutrition.aggregations import (
    generate_district_reports, generate_region_country_reports,
    generate_weekly_district_reports, generate_weekly_region_country_reports)

logger = logging.getLogger(__name__)


class Command(BaseCommand):

    def handle(self, *args, **options):

        logger.info("snisi_nutrition daily-checkups")

        now = timezone.now()
        today = now.date()
        day = now.day
        period = MonthPeriod.current().previous()

        category_matrix = {
            'end_of_reporting_period':
                end_of_reporting_period_notifications,
            'end_of_extended_reporting_period':
                end_of_extended_reporting_period_notifications,
            'performance_indicators':
                performance_indicators_notifications,
            'inputs_stockouts':
                inputs_stockouts_notifications,
            'end_of_district_period': generate_district_reports,
            'end_of_region_period': generate_region_country_reports,

            'end_of_weekly_district_period': generate_weekly_district_reports,
            'end_of_weekly_region_period':
                generate_weekly_region_country_reports,
        }

        def handle_category(category, custom_period=None):
            if custom_period is None:
                custom_period = period
            slug = "{domain}_{period}_{category}".format(
                domain=DOMAIN_SLUG,
                period=custom_period.strid(),
                category=category)
            task, created = PeriodicTask.get_or_create(slug, category)

            if task.can_trigger():
                try:
                    if category_matrix.get(category)(custom_period) \
                            is not False:
                        task.trigger()
                except Exception as e:
                    logger.error("Exception raised during aggregation.")
                    logger.exception(e)
            else:
                logger.debug("{} already triggered".format(task))

        # Monthly reports
        # On 6th
        if day >= ROUTINE_REPORTING_END_DAY:
            # send warning notice to non-satisfied HC person
            handle_category("end_of_reporting_period")
            pass

        # On 11th
        if day >= ROUTINE_EXTENDED_REPORTING_END_DAY:
            # send summary notification and validation invitatin to districts
            handle_category("end_of_extended_reporting_period")
            pass

        # On 16th
        if day >= ROUTINE_DISTRICT_AGG_DAY:
            # validate all HC reports
            # create aggregated for district
            # create expected-validation for district
            # send notification to regions
            handle_category("end_of_district_period")
            handle_category("performance_indicators")
            handle_category("inputs_stockouts")

        # On 26th
        if day >= ROUTINE_REGION_AGG_DAY:
            # validate all district reports
            # create aggregated for region
            # create aggregated for country
            # send notification to central/national
            handle_category("end_of_region_period")

        # WEEKLY REPORTS

        # number and position of weeks across month is inconsistent.
        # loop through potential past weeks and process if possible
        pf = NutWeekPeriod.find_create_by_date(period.following().start_on)
        pe = NutWeekPeriod.current()
        wperiods = [p for p in NutWeekPeriod.all_from(pf, pe)
                    if p.end_on < now]

        for wperiod in wperiods:
            # validate all HC reports
            # create aggregated for district
            # create expected-validation for district
            # send notification to regions
            if (wperiod.end_on + datetime.timedelta(
                    days=ROUTINE_DISTRICT_AGG_DAYS_DELTA)).date() <= today:
                handle_category("end_of_weekly_district_period", wperiod)

            # validate all district reports
            # create aggregated for region
            # create aggregated for country
            # send notification to central/national
            if (wperiod.end_on + datetime.timedelta(
                    days=ROUTINE_REGION_AGG_DAYS_DELTA)).date() <= today:
                handle_category("end_of_weekly_region_period", wperiod)
