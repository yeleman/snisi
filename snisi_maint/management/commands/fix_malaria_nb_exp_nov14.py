#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim: ai ts=4 sts=4 et sw=4 nu

from __future__ import (unicode_literals, absolute_import,
                        division, print_function)
import logging

from django.core.management.base import BaseCommand

from snisi_core.models.Periods import MonthPeriod
from snisi_malaria.models import AggMalariaR

logger = logging.getLogger(__name__)


class Command(BaseCommand):

    def handle(self, *args, **options):

        period = MonthPeriod.from_url_str("11-2014")

        for report in AggMalariaR.objects.filter(period=period):
            logger.info(report)
            report.update_expected_reportings_number()
            report.save()

        logger.info("All done.")
