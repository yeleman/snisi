#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim: ai ts=4 sts=4 et sw=4 nu

from __future__ import (unicode_literals, absolute_import,
                        division, print_function)
import logging

from snisi_core.models.Projects import Domain

logger = logging.getLogger(__name__)


PROJECT_BRAND = "NUT"
DOMAIN_SLUG = 'nutrition'

# Weekly reporting (Friday monring to thursday night)
# All deltas relativee to end of period
ROUTINE_REPORTING_END_DAYS_DELTA = 1
ROUTINE_EXTENDED_REPORTING_END_DAYS_DELTA = 3
ROUTINE_DISTRICT_AGG_DAYS_DELTA = 3
ROUTINE_REGION_AGG_DAYS_DELTA = 4

# Monthly reporting
ROUTINE_REPORTING_END_DAY = 6
ROUTINE_EXTENDED_REPORTING_END_DAY = 11
ROUTINE_DISTRICT_AGG_DAY = 16
ROUTINE_REGION_AGG_DAY = 26


def get_domain():
    return Domain.get_or_none(DOMAIN_SLUG)
