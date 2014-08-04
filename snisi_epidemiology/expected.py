#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim: ai ts=4 sts=4 et sw=4 nu

from __future__ import (unicode_literals, absolute_import,
                        division, print_function)
import logging
import copy
import datetime

from snisi_core.models.Periods import MonthPeriod
# from snisi_core.models.ReportingPeriods import (
#     DefaultMonthlyReportingPeriod, DefaultMonthlyExtendedReportingPeriod)
from snisi_core.models.Projects import Cluster
from snisi_core.models.Roles import Role
from snisi_core.models.Reporting import ExpectedReporting, ReportClass
from snisi_epidemiology import get_domain
from snisi_epidemiology.models import EpiWeekPeriod, EpiWeekReportingPeriod

logger = logging.getLogger(__name__)
DOMAIN = get_domain()

logger = logging.getLogger(__name__)
reportcls_pf = ReportClass.get_or_none(slug='epidemio_weekly_routine')
reportcls_pf_agg = ReportClass.get_or_none(
    slug='epidemio_weekly_routine_aggregated')


def create_expected_for(period):
    logger.info("Creating ExpectedReporting for {} at {}"
                .format(DOMAIN, period))

    created_list = []

    routine_cluster = Cluster.get_or_none("epidemiology_routine")

    dtc = Role.get_or_none("dtc")
    charge_sis = Role.get_or_none("charge_sis")

    expected_dict = {
        'period': None,
        'within_period': False,
        'within_entity': False,
        'reporting_role': dtc,
        'reporting_period': None,
        'extended_reporting_period': None,
        'amount_expected': ExpectedReporting.EXPECTED_SINGLE
    }

    # snisi_reprohealth only work with those periods
    if not period.__class__ == MonthPeriod:
        logger.debug("Period {} is not relevant to {}".format(period, DOMAIN))
        return created_list
    else:

        wperiods = list(set([EpiWeekPeriod.find_create_by_date(
            period.start_on + datetime.timedelta(days=d))
            for d in (1, 7, 14, 21, 28)]))

        for wperiod in wperiods:

            logger.info("wperiod")
            logger.info(wperiod)

            reporting_period = EpiWeekReportingPeriod.find_create_by_date(
                wperiod.middle())

            for entity in routine_cluster.members():

                # report class is based on indiv/agg
                reportcls = reportcls_pf \
                    if entity.type.slug == 'health_center' \
                    else reportcls_pf_agg
                reporting_role = dtc \
                    if entity.type.slug == 'health_center' else charge_sis

                edict = copy.copy(expected_dict)
                edict.update({
                    'entity': entity,
                    'period': wperiod,
                    'report_class': reportcls,
                    'reporting_role': reporting_role,
                    'reporting_period': reporting_period
                })

                finddict = copy.copy(edict)
                del(finddict['reporting_period'])
                del(finddict['extended_reporting_period'])

                e, created = ExpectedReporting.objects \
                    .get_or_create(**finddict)
                if created:
                    logger.debug("Created {}".format(e))
                    created_list.append(e)
                else:
                    logger.debug("Exists already: {}".format(e))
                if e.period != edict['period']:
                    e.period = edict['period']
                    e.save()
                if e.reporting_period != edict['reporting_period']:
                    e.reporting_period = edict['reporting_period']
                    e.save()
                if e.extended_reporting_period \
                        != edict['extended_reporting_period']:
                    e.extended_reporting_period \
                        = edict['extended_reporting_period']
                    e.save()

    return created_list


def report_classes_for(cluster):
    return [reportcls_pf, reportcls_pf_agg]
