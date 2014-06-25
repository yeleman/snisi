#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim: ai ts=4 sts=4 et sw=4 nu

from __future__ import (unicode_literals, absolute_import,
                        division, print_function)
import datetime
import logging

from django.core.management.base import BaseCommand
from django.utils import timezone

from snisi_core.models.Entities import Entity
from snisi_core.models.Periods import MonthPeriod
from snisi_core.models.Projects import Cluster, Participation
from snisi_tools.datetime import DEBUG_change_system_date

logger = logging.getLogger(__name__)

speriod = MonthPeriod.from_url_str("01-2013")
eperiod = MonthPeriod.from_url_str("12-2013")
periods = MonthPeriod.all_from(speriod, eperiod)


class Command(BaseCommand):

    def handle(self, *args, **options):

        coverage_cluster = Cluster.objects.get(slug="vacc_coverage_routine")
        DEBUG_change_system_date(
            MonthPeriod.from_url_str("12-2012").end_on - datetime.timedelta(days=5), True)

        mali = Entity.get_or_none("mali")

        regions = ['2732']

        health_units = [mali]
        for region_slug in regions:
            region = Entity.get_or_none(region_slug)
            health_units += [region] + region.get_health_districts() \
                                     + region.get_health_centers()

        for health_unit in health_units:
            logger.info(health_unit)

            p, created = Participation.objects.get_or_create(
                cluster=coverage_cluster,
                entity=health_unit,
                modified_on=timezone.now())

        DEBUG_change_system_date(None, True)
