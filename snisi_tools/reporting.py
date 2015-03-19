#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim: ai ts=4 sts=4 et sw=4 nu

from __future__ import (unicode_literals, absolute_import,
                        division, print_function)
import logging

from django.utils import timezone

from snisi_core.models.Periods import MonthPeriod

logger = logging.getLogger(__name__)


def routine_month_period_complete(period, domain, entity):
    region_eord = domain.import_from('ROUTINE_REGION_AGG_DAY')
    district_eord = domain.import_from('ROUTINE_DISTRICT_AGG_DAY')
    current = MonthPeriod.current()
    if period >= current:
        return False
    if period < current.previous():
        return True
    if entity.type.slug in ('country', 'region', 'health_district'):
        eord = region_eord
    else:
        eord = district_eord
    return timezone.now().day >= eord
