#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim: ai ts=4 sts=4 et sw=4 nu

from __future__ import (unicode_literals, absolute_import,
                        division, print_function)
import logging
import datetime

from django.core.management.base import BaseCommand
from django.utils import timezone

from snisi_tools.datetime import DEBUG_change_system_date
from snisi_core.models.PeriodicTasks import PeriodicTask
from snisi_nutrition import (DOMAIN_SLUG,
                             ROUTINE_DISTRICT_AGG_DAYS_DELTA,
                             ROUTINE_REGION_AGG_DAYS_DELTA)
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

        # number and position of weeks across month is inconsistent.
        # loop through potential past weeks and process if possible
        pf = NutWeekPeriod.find_create_by_date(datetime.datetime(2015, 1, 1))
        pl = NutWeekPeriod.current()
        wperiods = [p for p in NutWeekPeriod.all_from(pf, pl)
                    if p.end_on < now]

        for wperiod in wperiods:
            # validate all HC reports
            # create aggregated for district
            # create expected-validation for district
            # send notification to regions
            if (wperiod.end_on + datetime.timedelta(
                    days=ROUTINE_DISTRICT_AGG_DAYS_DELTA)).date() <= today:
                nd = (wperiod.end_on + datetime.timedelta(
                    days=ROUTINE_DISTRICT_AGG_DAYS_DELTA)).date()
                DEBUG_change_system_date(nd, True)
                handle_category("end_of_weekly_district_period", wperiod)

            # validate all district reports
            # create aggregated for region
            # create aggregated for country
            # send notification to central/national
            if (wperiod.end_on + datetime.timedelta(
                    days=ROUTINE_REGION_AGG_DAYS_DELTA)).date() <= today:
                nd = (wperiod.end_on + datetime.timedelta(
                    days=ROUTINE_REGION_AGG_DAYS_DELTA)).date()
                DEBUG_change_system_date(nd, True)
                handle_category("end_of_weekly_region_period", wperiod)
