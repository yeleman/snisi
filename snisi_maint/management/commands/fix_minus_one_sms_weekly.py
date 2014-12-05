#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim: ai ts=4 sts=4 et sw=4 nu

from __future__ import (unicode_literals, absolute_import,
                        division, print_function)
import logging

import reversion
from django.core.management.base import BaseCommand

from snisi_nutrition.models.Weekly import WeeklyNutritionR

logger = logging.getLogger(__name__)


class Command(BaseCommand):

    def handle(self, *args, **options):

        for report in WeeklyNutritionR.objects.all():
            logger.info(report)
            changed = False
            for field in report.data_fields():
                if getattr(report, field) == -1:
                    setattr(report, field, 0)
                    changed = True
            if changed:
                logger.info("\tCHANGED.")
                with reversion.create_revision():
                    report.save()
