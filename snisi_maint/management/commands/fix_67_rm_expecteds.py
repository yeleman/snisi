#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim: ai ts=4 sts=4 et sw=4 nu

from __future__ import (unicode_literals, absolute_import,
                        division, print_function)
import logging

from django.core.management.base import BaseCommand
from django.core.management import call_command

from snisi_core.models.Periods import MonthPeriod
from snisi_core.models.Entities import Entity
from snisi_core.models.Projects import Participation
from snisi_core.models.Reporting import (ExpectedReporting)

logger = logging.getLogger(__name__)


class Command(BaseCommand):

    def handle(self, *args, **options):

        logger.info("Issue #67. Removing expecteds for djenne entities.")

        january = MonthPeriod.from_url_str("12-2014")
        periods = MonthPeriod.all_from(january)
        entity_slugs = ['ANT9', 'M894', 'C332']

        for exp in ExpectedReporting.objects.filter(
                period__in=periods, entity__slug__in=entity_slugs):
            logger.debug(exp)
            exp.delete()

        logger.info("Disable health area if not already")
        for slug in entity_slugs:
            area_slug = "Z{}".format(slug)
            e = Entity.objects.get(slug=area_slug)
            if e and e.active:
                logger.info(e)
                e.active = False
                e.save()

        logger.info("Remove from clusters")
        Participation.objects.filter(entity__slug__in=entity_slugs).delete()

        logger.info("Update cluster cache")
        call_command("update-cluster-caches")

        logger.info("done.")
