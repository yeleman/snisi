#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim: ai ts=4 sts=4 et sw=4 nu

from __future__ import (unicode_literals, absolute_import,
                        division, print_function)
import logging

from snisi_core.models.Projects import Domain

logger = logging.getLogger(__name__)

PROJECT_BRAND = "SMIR"
DOMAIN_SLUG = 'epidemiology'

# epidemio is based on traditional weeks
# period ends on Friday noon and collect ends on Sunday noon.
# District validation by Monday noon
# Region validation by Tuesday noon
ROUTINE_REPORTING_END_WEEKDAY = 4  # Friday
ROUTINE_DISTRICT_AGG_DAYS_DELTA = 3
ROUTINE_REGION_AGG_DAYS_DELTA = 4


def get_domain():
    return Domain.get_or_none(DOMAIN_SLUG)
