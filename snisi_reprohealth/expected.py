#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim: ai ts=4 sts=4 et sw=4 nu

from __future__ import (unicode_literals, absolute_import,
                        division, print_function)
import logging
import copy
import datetime

from snisi_core.models.Periods import MonthPeriod, DayPeriod
from snisi_core.models.ReportingPeriods import (DefaultMonthlyReportingPeriod,
                                                DefaultMonthlyExtendedReportingPeriod)
from snisi_core.models.Projects import Cluster
from snisi_core.models.Roles import Role
from snisi_core.models.Reporting import ExpectedReporting, ReportClass
from snisi_reprohealth import get_domain

logger = logging.getLogger(__name__)
DOMAIN = get_domain()

logger = logging.getLogger(__name__)
reportcls_services = ReportClass.get_or_none(slug='msi_services_monthly_routine')
reportcls_services_agg = ReportClass.get_or_none(slug='msi_services_monthly_routine_aggregated')
reportcls_financial = ReportClass.get_or_none(slug='msi_financial_monthly_routine')
reportcls_financial_agg = ReportClass.get_or_none(slug='msi_financial_monthly_routine_aggregated')
reportcls_stocks = ReportClass.get_or_none(slug='msi_stocks_monthly_routine')
reportcls_stocks_agg = ReportClass.get_or_none(slug='msi_stocks_monthly_routine_aggregated')
all_report_classes = [
    (reportcls_services, reportcls_services_agg),
    (reportcls_financial, reportcls_financial_agg),
    (reportcls_stocks, reportcls_stocks_agg)
]


def create_expected_for(period):
    logger.info("Creating ExpectedReporting for {} at {}".format(DOMAIN, period))

    created_list = []

    routine_cluster = Cluster.get_or_none("msi_reprohealth_routine")

    dtc = Role.get_or_none("dtc")
    charge_sis = Role.get_or_none("charge_sis")

    expected_dict = {
        'period': period,
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
        reporting_period = DefaultMonthlyReportingPeriod \
            .find_create_by_date(period.following().middle())
        extended_reporting_period = DefaultMonthlyExtendedReportingPeriod \
            .find_create_by_date(period.following().middle())

        for entity in routine_cluster.members():

            for rptcls_indiv, rptcls_agg in all_report_classes:

                # report class is based on indiv/agg
                reportcls = rptcls_indiv \
                    if entity.type.slug == 'health_center' else rptcls_agg
                reporting_role = dtc if entity.type.slug == 'health_center' \
                                     else charge_sis

                edict = copy.copy(expected_dict)
                edict.update({
                    'entity': entity,
                    'report_class': reportcls,
                    'reporting_role': reporting_role,
                    'reporting_period': reporting_period,
                    'extended_reporting_period': extended_reporting_period,
                })

                finddict = copy.copy(edict)
                del(finddict['reporting_period'])
                del(finddict['extended_reporting_period'])

                e, created = ExpectedReporting.objects.get_or_create(**finddict)
                if created:
                    logger.debug("Created {}".format(e))
                    created_list.append(e)
                else:
                    logger.debug("Exists already: {}".format(e))
                if e.reporting_period != edict['reporting_period']:
                    e.reporting_period = edict['reporting_period']
                    e.save()
                if e.extended_reporting_period != edict['extended_reporting_period']:
                    e.extended_reporting_period = edict['extended_reporting_period']
                    e.save()

    return created_list


def report_classes_for(cluster):
    return [reportcls_services, reportcls_services_agg,
            reportcls_financial, reportcls_financial_agg,
            reportcls_stocks, reportcls_stocks_agg]
