#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim: ai ts=4 sts=4 et sw=4 nu

from __future__ import (unicode_literals, absolute_import,
                        division, print_function)
import logging

from django.core.management.base import BaseCommand
from django.utils import timezone

from snisi_malaria import (DOMAIN_SLUG,
                           ROUTINE_REPORTING_END_DAY,
                           ROUTINE_EXTENDED_REPORTING_END_DAY,
                           ROUTINE_DISTRICT_AGG_DAY,
                           ROUTINE_REGION_AGG_DAY)
from snisi_core.models.PeriodicTasks import PeriodicTask
from snisi_malaria.aggregations import (generate_district_reports,
                                        generate_region_country_reports,
                                        generate_weekly_reports)
from snisi_malaria.notifications import (
    end_of_reporting_period_notifications,
    end_of_extended_reporting_period_notifications)
from snisi_core.models.Periods import MonthPeriod
from snisi_core.models.FixedWeekPeriods import (
    FixedMonthWeek,
    FixedMonthFirstWeek,
    FixedMonthSecondWeek,
    FixedMonthThirdWeek,
    FixedMonthFourthWeek,
    FixedMonthFifthWeek)

logger = logging.getLogger(__name__)


class Command(BaseCommand):

    def handle(self, *args, **options):

        logger.info("snisi_malaria daily-checkups")

        day = timezone.now().day
        period = MonthPeriod.current().previous()
        this_month = period.following()
        # period_str = period.strid()
        wperiod = FixedMonthWeek.previous_week(FixedMonthWeek.current())
        # wperiod_str = MonthPeriod.current().strid()
        logger.debug("{} -- {}".format(period, wperiod))

        category_matrix = {
            'end_of_reporting_period': end_of_reporting_period_notifications,
            'end_of_extended_reporting_period':
                end_of_extended_reporting_period_notifications,
            'end_of_district_period': generate_district_reports,
            'end_of_region_period': generate_region_country_reports,
            'end_of_first_week_period_reporting': generate_weekly_reports,
            'end_of_second_week_period_reporting': generate_weekly_reports,
            'end_of_third_week_period_reporting': generate_weekly_reports,
            'end_of_fourth_week_period_reporting': generate_weekly_reports,
            'end_of_fifth_week_period_reporting': generate_weekly_reports,
        }

        def handle_category(category, nperiod=None, wperiod=None):
            if nperiod is None:
                nperiod = period
            slug = "{domain}_{period}_{category}".format(
                domain=DOMAIN_SLUG, period=nperiod.strid(), category=category)
            task, created = PeriodicTask.get_or_create(slug, category)

            if task.can_trigger():
                logger.debug("triggering {}".format(task))
                try:
                    category_matrix.get(category)(period=nperiod,
                                                  wperiod=wperiod)
                except Exception as e:
                    logger.exception(e)
                else:
                    task.trigger()
            else:
                logger.info("{} already triggered".format(task))

        # On 1st
        if day >= 1:
            # in case we had only 28 days last month
            wperiod = FixedMonthFourthWeek.find_create_from(
                period.middle().year, period.middle().month)
            handle_category("end_of_fourth_week_period_reporting",
                            period, wperiod)
            wperiod = FixedMonthFifthWeek.find_create_from(
                period.middle().year, period.middle().month)
            handle_category("end_of_fifth_week_period_reporting",
                            period, wperiod)

        # On 6th
        if day >= ROUTINE_REPORTING_END_DAY:
            # send warning notice to non-satisfied HC person
            handle_category("end_of_reporting_period")

        # On 11th
        if day >= ROUTINE_EXTENDED_REPORTING_END_DAY:
            # send summary notification and validation invitatin to districts
            handle_category("end_of_extended_reporting_period")

        # On 13th
        if day >= 13:
            wperiod = FixedMonthFirstWeek.find_create_from(
                period.following().middle().year,
                period.following().middle().month)
            handle_category("end_of_first_week_period_reporting",
                            this_month, wperiod)

        # On 16th
        if day >= ROUTINE_DISTRICT_AGG_DAY:
            # validate all HC reports
            # create aggregated for district
            # create expected-validation for district
            # send notification to regions
            handle_category("end_of_district_period")

        # On 20th
        if day >= 20:
            wperiod = FixedMonthSecondWeek.find_create_from(
                period.following().middle().year,
                period.following().middle().month)
            handle_category("end_of_second_week_period_reporting",
                            this_month, wperiod)

        # On 26th
        if day >= ROUTINE_REGION_AGG_DAY:
            # validate all district reports
            # create aggregated for region
            # create aggregated for country
            # send notification to central/national
            handle_category("end_of_region_period")

        # On 27th
        if day >= 27:
            wperiod = FixedMonthThirdWeek.find_create_from(
                period.following().middle().year,
                period.following().middle().month)
            handle_category("end_of_third_week_period_reporting",
                            this_month, wperiod)
