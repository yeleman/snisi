#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim: ai ts=4 sts=4 et sw=4 nu

from __future__ import (unicode_literals, absolute_import,
                        division, print_function)
import logging

from django.core.management.base import BaseCommand
from django.utils import timezone

from snisi_core.models.Periods import MonthPeriod
from snisi_core.models.Reporting import ExpectedReporting, ExpectedValidation
from snisi_nutrition.models.Monthly import NutritionR
from snisi_nutrition.models.URENAM import URENAMNutritionR
from snisi_nutrition.models.URENAS import URENASNutritionR
from snisi_nutrition.models.URENI import URENINutritionR
from snisi_nutrition.models.Stocks import NutritionStocksR

logger = logging.getLogger(__name__)


class Command(BaseCommand):

    def handle(self, *args, **options):

        period = MonthPeriod.from_url_str("11-2014")

        logger.info(NutritionR.objects.filter(period=period).count())

        ok_slugs = [r['entity']
                    for r in
                    NutritionR.objects.filter(period=period).values('entity')]

        for r in URENAMNutritionR.objects.filter(period=period):
            if r.entity.slug not in ok_slugs:
                logger.debug(r)
                exp = ExpectedReporting.objects.get(
                    report_class__slug='nut_urenam_monthly_routine',
                    period=period,
                    entity__slug=r.entity.slug)
                exp.arrived_reports.remove(r)
                exp.completion_status = exp.COMPLETION_MISSING
                exp.save()
                exp.updated_on = timezone.now()

                try:
                    expv = ExpectedValidation.objects.get(report=r)
                    expv.delete()
                except:
                    pass

                r.delete()

        for r in URENASNutritionR.objects.filter(period=period):
            if r.entity.slug not in ok_slugs:
                logger.debug(r)
                exp = ExpectedReporting.objects.get(
                    report_class__slug='nut_urenas_monthly_routine',
                    period=period,
                    entity__slug=r.entity.slug)
                exp.arrived_reports.remove(r)
                exp.completion_status = exp.COMPLETION_MISSING
                exp.save()
                exp.updated_on = timezone.now()

                try:
                    expv = ExpectedValidation.objects.get(report=r)
                    expv.delete()
                except:
                    pass

                r.delete()

        for r in URENINutritionR.objects.filter(period=period):
            if r.entity.slug not in ok_slugs:
                logger.debug(r)
                exp = ExpectedReporting.objects.get(
                    report_class__slug='nut_ureni_monthly_routine',
                    period=period,
                    entity__slug=r.entity.slug)
                exp.arrived_reports.remove(r)
                exp.completion_status = exp.COMPLETION_MISSING
                exp.save()
                exp.updated_on = timezone.now()

                try:
                    expv = ExpectedValidation.objects.get(report=r)
                    expv.delete()
                except:
                    pass

                r.delete()

        for r in NutritionStocksR.objects.filter(period=period):
            if r.entity.slug not in ok_slugs:
                logger.debug(r)
                exp = ExpectedReporting.objects.get(
                    report_class__slug='nut_stocks_monthly_routine',
                    period=period,
                    entity__slug=r.entity.slug)
                exp.arrived_reports.remove(r)
                exp.completion_status = exp.COMPLETION_MISSING
                exp.save()
                exp.updated_on = timezone.now()

                try:
                    expv = ExpectedValidation.objects.get(report=r)
                    expv.delete()
                except:
                    pass

                r.delete()

        logger.info(NutritionR.objects.filter(period=period).count())

