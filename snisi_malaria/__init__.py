#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim: ai ts=4 sts=4 et sw=4 nu

from __future__ import (unicode_literals, absolute_import,
                        division, print_function)

from snisi_core.models.Projects import Domain

PROJECT_BRAND = "PALU"
DOMAIN_SLUG = 'malaria'

ROUTINE_REPORTING_END_DAY = 6
ROUTINE_EXTENDED_REPORTING_END_DAY = 11
ROUTINE_DISTRICT_AGG_DAY = 16
ROUTINE_REGION_AGG_DAY = 26


def get_domain():
    return Domain.get_or_none(DOMAIN_SLUG)
