#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim: ai ts=4 sts=4 et sw=4 nu

from __future__ import (unicode_literals, absolute_import,
                        division, print_function)
import logging
import copy
import datetime

from snisi_core.models.Periods import MonthPeriod
from snisi_core.models.ReportingPeriods import (
    DefaultMonthlyReportingPeriod, DefaultMonthlyExtendedReportingPeriod)
from snisi_core.models.Projects import Cluster
from snisi_core.models.Roles import Role
from snisi_core.models.Reporting import ExpectedReporting, ReportClass
from snisi_nutrition.models.Weekly import (
    NutWeekPeriod, NutWeekReportingPeriod, NutWeekExtendedReportingPeriod)
from snisi_nutrition import get_domain

logger = logging.getLogger(__name__)
DOMAIN = get_domain()

logger = logging.getLogger(__name__)
reportcls_weekly = ReportClass.get_or_none(slug='nutrition_weekly_routine')
reportcls_weekly_agg = ReportClass.get_or_none(
    slug='nutrition_weekly_routine_aggregated')
reportcls_nut = ReportClass.get_or_none(slug='nutrition_monthly_routine')
reportcls_nut_agg = ReportClass.get_or_none(
    slug='nutrition_monthly_routine_aggregated')
reportcls_urenam = ReportClass.get_or_none(slug='nut_urenam_monthly_routine')
reportcls_urenam_agg = ReportClass.get_or_none(
    slug='nut_urenam_monthly_routine_aggregated')
reportcls_urenas = ReportClass.get_or_none(slug='nut_urenas_monthly_routine')
reportcls_urenas_agg = ReportClass.get_or_none(
    slug='nut_urenas_monthly_routine_aggregated')
reportcls_ureni = ReportClass.get_or_none(slug='nut_ureni_monthly_routine')
reportcls_ureni_agg = ReportClass.get_or_none(
    slug='nut_ureni_monthly_routine_aggregated')
reportcls_stocks = ReportClass.get_or_none(slug='nut_stocks_monthly_routine')
reportcls_stocks_agg = ReportClass.get_or_none(
    slug='nut_stocks_monthly_routine_aggregated')


def handle_entity(entity,
                  period,
                  expected_dict,
                  reportcls, reporting_role,
                  reporting_period, extended_reporting_period,
                  created_list):

    edict = copy.copy(expected_dict)
    edict.update({
        'period': period,
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
    if e.extended_reporting_period \
            != edict['extended_reporting_period']:
        e.extended_reporting_period \
            = edict['extended_reporting_period']
        e.save()
    if not e.completion_status:
        e.completion_status = ExpectedReporting.COMPLETION_MISSING
        e.save()


def create_expected_for(period):
    logger.info("Creating ExpectedReporting for {} at {}"
                .format(DOMAIN, period))

    created_list = []

    routine_cluster = Cluster.get_or_none("nutrition_routine")

    dtc = Role.get_or_none("dtc")
    charge_sis = Role.get_or_none("charge_sis")

    expected_dict = {
        'period': period,
        'within_period': False,
        'within_entity': False,
        'reporting_role': dtc,
        'reporting_period': None,
        'extended_reporting_period': None,
        'amount_expected': ExpectedReporting.EXPECTED_SINGLE,
    }

    report_classes = [
        ('urenam', reportcls_urenam, reportcls_urenam_agg),
        ('urenas', reportcls_urenas, reportcls_urenas_agg),
        ('ureni', reportcls_ureni, reportcls_ureni_agg),
        ('stocks', reportcls_stocks, reportcls_stocks_agg),
    ]

    # snisi_nutrition only work with those periods
    if not period.__class__ == MonthPeriod:
        logger.debug("Period {} is not relevant to {}".format(period, DOMAIN))
        return created_list
    else:
        reporting_period = DefaultMonthlyReportingPeriod \
            .find_create_by_date(period.following().middle())
        extended_reporting_period = DefaultMonthlyExtendedReportingPeriod \
            .find_create_by_date(period.following().middle())

        for entity in routine_cluster.members():

            # report class is based on indiv/agg
            reporting_role = dtc if entity.type.slug == 'health_center' \
                else charge_sis

            # URENAM, URENAS, URENI, STOCKS
            for uren, rcls, rcls_agg in report_classes:

                if entity.type.slug == 'health_center':
                    reportcls = rcls
                    # only create expected if entity has UREN
                    if uren != 'stocks' and not getattr(
                            entity, 'has_{}'.format(uren), False):
                        continue
                else:
                    reportcls = rcls_agg

                handle_entity(
                    entity=entity,
                    period=period,
                    expected_dict=expected_dict,
                    reportcls=reportcls,
                    reporting_role=reporting_role,
                    reporting_period=reporting_period,
                    extended_reporting_period=extended_reporting_period,
                    created_list=created_list)

            # NutritionR / AggNutritionR
            reportcls = reportcls_nut if entity.type.slug == 'health_center' \
                else reportcls_nut_agg
            handle_entity(
                entity=entity,
                period=period,
                expected_dict=expected_dict,
                reportcls=reportcls,
                reporting_role=reporting_role,
                reporting_period=reporting_period,
                extended_reporting_period=extended_reporting_period,
                created_list=created_list)

        # WEEKLY REPORTS

        # Weekly reportings apply to current month, not previous
        period = period.following()

        wperiods = list(set([NutWeekPeriod.find_create_by_date(
            period.start_on + datetime.timedelta(days=d))
            for d in (1, 7, 14, 21, 28)]))

        for wperiod in wperiods:

            logger.info(wperiod)

            reporting_period = NutWeekReportingPeriod.find_create_by_date(
                wperiod.middle())
            extended_reporting_period = NutWeekExtendedReportingPeriod \
                .find_create_by_date(wperiod.middle())

            for entity in routine_cluster.members():

                # report class is based on indiv/agg
                reportcls = reportcls_weekly \
                    if entity.type.slug == 'health_center' \
                    else reportcls_weekly_agg
                reporting_role = dtc \
                    if entity.type.slug == 'health_center' else charge_sis

                handle_entity(
                    entity=entity,
                    period=wperiod,
                    expected_dict=expected_dict,
                    reportcls=reportcls,
                    reporting_role=reporting_role,
                    reporting_period=reporting_period,
                    extended_reporting_period=extended_reporting_period,
                    created_list=created_list)

    return created_list


def report_classes_for(cluster):
    return [reportcls_nut, reportcls_nut_agg]
