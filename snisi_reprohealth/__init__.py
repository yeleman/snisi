#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim: ai ts=4 sts=4 et sw=4 nu

from __future__ import (unicode_literals, absolute_import,
                        division, print_function)
import logging

from snisi_core.models.Projects import Domain

logger = logging.getLogger(__name__)


PROJECT_BRAND = "PF"
DOMAIN_SLUG = 'reprohealth'

ROUTINE_REPORTING_END_DAY = 6
ROUTINE_EXTENDED_REPORTING_END_DAY = 11
ROUTINE_DISTRICT_AGG_DAY = 11
ROUTINE_REGION_AGG_DAY = 11


def get_domain():
    return Domain.get_or_none(DOMAIN_SLUG)
