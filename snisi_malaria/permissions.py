#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim: ai ts=4 sts=4 et sw=4 nu

from __future__ import (unicode_literals, absolute_import,
                        division, print_function)
import logging

from snisi_malaria import get_domain

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

    # Point Focal Palu
    if prole == 'pf_palu':

        # ensure at district
        if not plocation == plocation.get_health_disctrict():
            return

        # can upload report for HC within district
        if action == 'create-report':
            return location in plocation.get_health_centers()

        # can view data from the district
        if action in ('access', 'download'):
            return location in plocation.get_health_centers() + [plocation]

    # Chargé SIS
    if prole == 'charge_sis':

        # Region based
        if plocation == plocation.get_health_region():

            # can edit and validate districts reports
            if action in ('edit-report', 'validate-report'):
                return location in plocation.get_health_disctricts()

            # can view data from the district
            if action in ('access', 'download'):
                return location in plocation.get_health_centers() \
                    + plocation.get_health_disctricts() + [plocation]

        # District based
        elif plocation == plocation.get_health_disctrict():

            # can upload report for HC within district
            if action in ('create-report', 'edit-report', 'validate-report'):
                return location in plocation.get_health_centers()

            # can view data from the district
            if action in ('access', 'download'):
                return location in plocation.get_health_centers() + [plocation]

        # Not handled
        else:
            return
