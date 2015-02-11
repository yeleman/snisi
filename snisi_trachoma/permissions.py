#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim: ai ts=4 sts=4 et sw=4 nu

from __future__ import (unicode_literals, absolute_import,
                        division, print_function)
import logging

from snisi_trachoma import get_domain

logger = logging.getLogger(__name__)


def provider_is_allowed(prole, plocation, privileges,
                        location, action, domain, extension):

    # malaria-specific permissions only
    if not domain == get_domain():
        return

    # DTC
    if prole in ('tt_opt', 'tt_amo', 'tt_tso'):

        # can create report for their own HC
        if action == 'create-report':

            # District based
            if plocation == plocation.get_health_district():

                # can upload report for villages within district and district
                if action in ('create-report'):
                    return location in plocation.get_villages() + [location]

            # Not handled
            else:
                return
