#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim: ai ts=4 sts=4 et sw=4 nu

from __future__ import (unicode_literals, absolute_import,
                        division, print_function)
import logging

from snisi_nutrition import get_domain

logger = logging.getLogger(__name__)


def provider_is_allowed(prole, plocation, privileges,
                        location, action, domain, extension):
    # malaria-specific permissions only
    if not domain == get_domain():
        return

    # DTC & Chargé NUT (CSRef)
    if prole in ('dtc', 'charge_nut'):

        # can create report for their own HC
        if action == 'create-report':
            return plocation == location

    # Point Focal NUT (Privilege)
    if privileges.get('pf_nut'):

        pf_nut_location = privileges.get('pf_nut')

        # ensure at district
        if not pf_nut_location == pf_nut_location.get_health_district():
            return

        # can view data from the district
        if action in ('access', 'download'):
            return location in pf_nut_location.get_health_centers() \
                + [pf_nut_location]

    # Chargé SIS
    if prole == 'charge_sis':

        # Region based
        if plocation == plocation.get_health_region():

            # can edit and validate districts reports
            if action in ('edit-report', 'validate-report'):
                return location in plocation.get_health_districts()

            # can view data from the district
            if action in ('access', 'download'):
                return location in plocation.get_health_centers() \
                    + plocation.get_health_districts() + [plocation]

        # District based
        elif plocation == plocation.get_health_district():

            # can upload report for HC within district
            if action in ('create-report', 'edit-report', 'validate-report'):
                return location in plocation.get_health_centers()

            # can view data from the district
            if action in ('access', 'download'):
                return location in plocation.get_health_centers() + [plocation]

        # Not handled
        else:
            return
