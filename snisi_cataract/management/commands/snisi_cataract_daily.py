#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim: ai ts=4 sts=4 et sw=4 nu

from __future__ import (unicode_literals, absolute_import,
                        division, print_function)
import logging

from django.core.management.base import BaseCommand
from django.utils import timezone

from snisi_core.models.Periods import MonthPeriod
from snisi_core.models.PeriodicTasks import PeriodicTask
from snisi_cataract import (DOMAIN_SLUG, ROUTINE_REGION_AGG_DAY)
from snisi_cataract.aggregations import generate_aggregated_reports

logger = logging.getLogger(__name__)


class Command(BaseCommand):

    def handle(self, *args, **options):

        logger.info("snisi_cataract daily-checkups")

        day = timezone.now().day
        period = MonthPeriod.current()

        category_matrix = {
            'end_of_cataract_mission_period': generate_aggregated_reports,
        }

        def handle_category(category):
            slug = "{domain}_{period}_{category}".format(
                domain=DOMAIN_SLUG, period=period.strid(), category=category)
            task, created = PeriodicTask.get_or_create(slug, category)

            if task.can_trigger():
                category_matrix.get(category)(period)
                task.trigger()

        if day >= ROUTINE_REGION_AGG_DAY:
            # validate all district reports
            # create aggregated for region
            # create aggregated for country
            # send notification to central/national
            handle_category("end_of_cataract_mission_period")
