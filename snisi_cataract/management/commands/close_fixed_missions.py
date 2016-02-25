#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim: ai ts=4 sts=4 et sw=4 nu

from __future__ import (unicode_literals, absolute_import,
                        division, print_function)
import logging

from django.utils import timezone
from django.core.management.base import BaseCommand

from snisi_cataract.models import CATMissionR, FIXED
from snisi_core.models.Periods import MonthPeriod


logger = logging.getLogger(__name__)


class Command(BaseCommand):

    def handle(self, *args, **options):

        period = MonthPeriod.current()
        now = timezone.now()
        if not period.end_on < now:
            logger.error("Can not close mission before end of period")
            # return

        for mission in CATMissionR.objects.filter(strategy=FIXED,
                                                  period=period):
            logger.info("Closing {}".format(mission))
            mission.close(period.end_on.date())

        logger.info("All Done")
