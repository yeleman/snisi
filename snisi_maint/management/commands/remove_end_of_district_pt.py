#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim: ai ts=4 sts=4 et sw=4 nu

from __future__ import (unicode_literals, absolute_import,
                        division, print_function)
import logging

from django.core.management.base import BaseCommand

from snisi_core.models.Periods import MonthPeriod
from snisi_core.models.PeriodicTasks import PeriodicTask

logger = logging.getLogger(__name__)


class Command(BaseCommand):

    def handle(self, *args, **options):

        period = MonthPeriod.current().previous()
        category = 'end_of_district_period'

        for pt in PeriodicTask.objects.filter(category=category):
            regexp = r'_{p}_{cat}'.format(p=period.strid(), cat=category)
            if not pt.slug.endswith(regexp):
                continue

            # skipping nutrition
            if pt.slug == 'nutrition_12-2014_end_of_district_period':
                continue

            logger.info("Untriggering {}".format(pt))
            pt.untrigger()
