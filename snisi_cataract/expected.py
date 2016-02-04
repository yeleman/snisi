#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim: ai ts=4 sts=4 et sw=4 nu

from __future__ import (unicode_literals, absolute_import,
                        division, print_function)
import logging
import copy

from snisi_core.models.Periods import MonthPeriod
from snisi_core.models.Projects import Cluster
from snisi_core.models.Reporting import ExpectedReporting, ReportClass
from snisi_cataract import get_domain

logger = logging.getLogger(__name__)
DOMAIN = get_domain()

mission_report_class = ReportClass.get_or_none("cat_mission")


def create_expected_for(period):

    # Cataract mission are created for current month
    # which corresponds to period.following()
    logger.info("Using period from {} to {} for Cataract."
                .format(period, period.following()))

    period = period.following()

    logger.info("Creating ExpectedReporting for {} at {}"
                .format(DOMAIN, period))

    created_list = []

    cataract_cluster = Cluster.get_or_none("cataract")

    expected_dict = {
        'period': period,
        'within_period': True,
        'within_entity': False,
        'reporting_role': None,
        'report_class': mission_report_class,
        'reporting_period': None,
        'extended_reporting_period': None,
        'amount_expected': ExpectedReporting.EXPECTED_ZEROPLUS,
    }

    # snisi_cataract only work with those periods
    if period.__class__ not in (MonthPeriod,):
        logger.debug("Period {} is not relevant to {}".format(period, DOMAIN))
        return created_list

    if period.__class__ == MonthPeriod:

        for entity in cataract_cluster.members(only_active=True):

            edict = copy.copy(expected_dict)
            edict.update({
                'entity': entity,
            })

            finddict = copy.copy(edict)

            e, created = ExpectedReporting.objects.get_or_create(**finddict)
            if created:
                logger.debug("Created {}".format(e))
                created_list.append(e)
            else:
                logger.debug("Exists already: {}".format(e))
            if not e.completion_status:
                e.completion_status = ExpectedReporting.COMPLETION_MISSING
                e.save()

    return created_list


def report_classes_for(cluster):
    return [mission_report_class]
