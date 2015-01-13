#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim: ai ts=4 sts=4 et sw=4 nu

from __future__ import (unicode_literals, absolute_import,
                        division, print_function)
import logging

from django.core.management.base import BaseCommand

from snisi_core.models.Periods import MonthPeriod
from snisi_core.models.Reporting import (ExpectedReporting)

logger = logging.getLogger(__name__)


class Command(BaseCommand):

    def handle(self, *args, **options):

        logger.info("Issue #58. Removing expecteds for 4 djenne entities.")

        december = MonthPeriod.from_url_str("12-2014")
        periods = MonthPeriod.all_from(december)
        entity_slugs = ['GG71', 'NBJ0', 'M894', 'C332']

        for exp in ExpectedReporting.objects.filter(
                period__in=periods, entity__slug__in=entity_slugs):
            logger.debug(exp)
            exp.delete()

        logger.info("done.")
