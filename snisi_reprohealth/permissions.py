#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim: ai ts=4 sts=4 et sw=4 nu

from __future__ import (unicode_literals, absolute_import,
                        division, print_function)
import logging

from snisi_reprohealth import get_domain

logger = logging.getLogger(__name__)


def provider_is_allowed(prole, plocation, privileges,
                        location, action, domain, extension):

    # malaria-specific permissions only
    if not domain == get_domain():
        return

    # DTC
    if prole == 'dtc':

        # can create report for their own HC
        if action == 'create-report':
            return plocation == location

    # Chargé SIS
    if prole == 'charge_sis':

        # District based
        if plocation == plocation.get_health_disctrict():

            # can upload report for HC within district
            if action in ('create-report'):
                return location in plocation.get_health_centers()

        # Not handled
        else:
            return
