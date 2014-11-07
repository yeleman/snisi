#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim: ai ts=4 sts=4 et sw=4 nu

from __future__ import (unicode_literals, absolute_import,
                        division, print_function)
import logging

from django.core.management.base import BaseCommand
from django.utils import timezone

from snisi_reprohealth import (DOMAIN_SLUG,
                               ROUTINE_REPORTING_END_DAY,
                               ROUTINE_EXTENDED_REPORTING_END_DAY,
                               ROUTINE_DISTRICT_AGG_DAY,
                               ROUTINE_REGION_AGG_DAY)
from snisi_core.models.PeriodicTasks import PeriodicTask
from snisi_reprohealth.aggregations import (generate_district_reports,
                                            generate_region_country_reports)
from snisi_reprohealth.notifications import (
    end_of_reporting_period_notifications,
    end_of_extended_reporting_period_notifications)
from snisi_core.models.Periods import MonthPeriod

logger = logging.getLogger(__name__)


class Command(BaseCommand):

    def handle(self, *args, **options):

        logger.info("snisi_reprohealth daily-checkups")

        day = timezone.now().day
        period = MonthPeriod.current().previous()
        period_str = period.strid()

        category_matrix = {
            'end_of_reporting_period': end_of_reporting_period_notifications,
            'end_of_extended_reporting_period':
                end_of_extended_reporting_period_notifications,
            'end_of_district_period': generate_district_reports,
            'end_of_region_period': generate_region_country_reports,
        }

        def handle_category(category):
            slug = "{domain}_{period}_{category}".format(
                domain=DOMAIN_SLUG, period=period_str, category=category)
            task, created = PeriodicTask.get_or_create(slug, category)

            if task.can_trigger():
                category_matrix.get(category)(period)
                task.trigger()

        # On 6th
        if day >= ROUTINE_REPORTING_END_DAY:
            # send warning notice to non-satisfied HC person
            handle_category("end_of_reporting_period")

        # On 11th
        if day >= ROUTINE_EXTENDED_REPORTING_END_DAY:
            # send summary notification and validation invitatin to districts
            handle_category("end_of_extended_reporting_period")

        # On 11th
        if day >= ROUTINE_DISTRICT_AGG_DAY:
            # validate all HC reports
            # create aggregated for district
            # create expected-validation for district
            # send notification to regions
            handle_category("end_of_district_period")

        # On 11th
        if day >= ROUTINE_REGION_AGG_DAY:
            # validate all district reports
            # create aggregated for region
            # create aggregated for country
            # send notification to central/national
            handle_category("end_of_region_period")
