#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim: ai ts=4 sts=4 et sw=4 nu

from __future__ import (unicode_literals, absolute_import,
                        division, print_function)
import logging
import copy
import datetime
from collections import OrderedDict

from snisi_core.models.Periods import MonthPeriod, DayPeriod
from snisi_core.models.FixedWeekPeriods import (FixedMonthFirstWeek,
                                                FixedMonthSecondWeek,
                                                FixedMonthThirdWeek,
                                                FixedMonthFourthWeek,
                                                FixedMonthFifthWeek)
from snisi_core.models.ReportingPeriods import (
    DefaultMonthlyReportingPeriod, DefaultMonthlyExtendedReportingPeriod,
    FixedMonthFirstWeekReportingPeriod, FixedMonthSecondWeekReportingPeriod,
    FixedMonthThirdWeekReportingPeriod, FixedMonthFourthWeekReportingPeriod,
    FixedMonthFifthWeekReportingPeriod,
    FixedMonthFirstWeekExtendedReportingPeriod,
    FixedMonthSecondWeekExtendedReportingPeriod,
    FixedMonthThirdWeekExtendedReportingPeriod,
    FixedMonthFourthWeekExtendedReportingPeriod,
    FixedMonthFifthWeekExtendedReportingPeriod)
from snisi_core.models.Projects import Cluster
from snisi_core.models.Roles import Role
from snisi_core.models.Reporting import ExpectedReporting, ReportClass
from snisi_malaria import get_domain

logger = logging.getLogger(__name__)
DOMAIN = get_domain()

indiv_report_class = ReportClass.get_or_none("malaria_monthly_routine")
agg_report_class = ReportClass.get_or_none(
    "malaria_monthly_routine_aggregated")
# episrc_report_class = ReportClass.get_or_none("malaria_weekly_epidemio")
routinesrc_report_class = ReportClass.get_or_none("malaria_weekly_routine")
routineagg_report_class = ReportClass.get_or_none(
    "malaria_weekly_routine_aggregated")
routineagg_week_report_class = ReportClass.get_or_none(
    "malaria_weekly_weeklong_routine_aggregated")
mwrfwa_report_class = ReportClass.get_or_none(
    "malaria_weekly_routine_firstweek_aggregated")
mwrswa_report_class = ReportClass.get_or_none(
    "malaria_weekly_routine_secondweek_aggregated")
mwrtwa_report_class = ReportClass.get_or_none(
    "malaria_weekly_routine_thirdweek_aggregated")
mwrfowa_report_class = ReportClass.get_or_none(
    "malaria_weekly_routine_fourthweek_aggregated")
mwrfiwa_report_class = ReportClass.get_or_none(
    "malaria_weekly_routine_fifthweek_aggregated")
mwrfwwa_report_class = ReportClass.get_or_none(
    "malaria_weekly_routine_firstweek_weeklong_aggregated")
mwrswwa_report_class = ReportClass.get_or_none(
    "malaria_weekly_routine_secondweek_weeklong_aggregated")
mwrtwwa_report_class = ReportClass.get_or_none(
    "malaria_weekly_routine_thirdweek_weeklong_aggregated")
mwrfowwa_report_class = ReportClass.get_or_none(
    "malaria_weekly_routine_fourthweek_weeklong_aggregated")
mwrfiwwa_report_class = ReportClass.get_or_none(
    "malaria_weekly_routine_fifthweek_weeklong_aggregated")


def create_expected_for(period):

    logger.info("Creating ExpectedReporting for {} at {}"
                .format(DOMAIN, period))

    created_list = []

    routine_cluster = Cluster.get_or_none("malaria_monthly_routine")

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

    # snisi_malaria only work with those periods
    if period.__class__ not in (MonthPeriod, DayPeriod,
                                FixedMonthFirstWeek, FixedMonthSecondWeek,
                                FixedMonthThirdWeek, FixedMonthFourthWeek,
                                FixedMonthFifthWeek):
        logger.debug("Period {} is not relevant to {}".format(period, DOMAIN))
        return created_list

    if period.__class__ == MonthPeriod:
        # Routine Malaria: INDIV or AGG reports
        reporting_period = DefaultMonthlyReportingPeriod \
            .find_create_by_date(period.following().middle())
        extended_reporting_period = DefaultMonthlyExtendedReportingPeriod \
            .find_create_by_date(period.following().middle())

        for entity in routine_cluster.members(only_active=True):

            # report class is based on indiv/agg
            reportcls = indiv_report_class \
                if entity.type.slug == 'health_center' else agg_report_class
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
            if e.extended_reporting_period \
                    != edict['extended_reporting_period']:
                e.extended_reporting_period = \
                    edict['extended_reporting_period']
                e.save()
            if not e.completion_status:
                e.completion_status = ExpectedReporting.COMPLETION_MISSING
                e.save()

        # create DayPeriod for Epidemiology for each day of the month
        # WARN: Weekly Epi applies to the current month and not the previous
        # one.
        # In routine, we expect at month N to receive month N-1.
        # In weekly, we expect at month N to receive weeks of month N
        # this function being called with N-1 period as parameter
        # we need to jump into the future N (so N+1) to create expecteds
        next_period = period.following()
        nb_day_in_month = ((next_period.end_on - next_period.start_on)
                           + datetime.timedelta(seconds=1)).days

        # ###
        # # EPIDEMIO
        # ###
        # epidemio_cluster = Cluster.get_or_none("malaria_weekly_epidemiology")
        # for day in range(1, nb_day_in_month + 1):
        #     day_period = DayPeriod.find_create_from(
        #         year=next_period.start_on.year,
        #         month=next_period.start_on.month, day=day)

        #     logger.debug("Generating DayPeriod Expecteds for {}"
        #                  .format(day_period))

        #     for entity in epidemio_cluster.members(only_active=True):

        #         edict = copy.copy(expected_dict)
        #         edict.update({
        #             'entity': entity,
        #             'period': day_period,
        #             'report_class': episrc_report_class,
        #             'reporting_period': None,
        #             'extended_reporting_period': None,
        #         })
        #         e, created = ExpectedReporting.objects.get_or_create(**edict)
        #         if created:
        #             logger.debug("Created {}".format(e))
        #             created_list.append(e)
        #         else:
        #             logger.debug("Exists already: {}".format(e))

        # # create FixedWeekPeriods for Epidemiology for the month
        # week_repperiod_matrix = OrderedDict([
        #     (FixedMonthFirstWeek, FixedMonthFirstWeekReportingPeriod),
        #     (FixedMonthSecondWeek, FixedMonthSecondWeekReportingPeriod),
        #     (FixedMonthThirdWeek, FixedMonthThirdWeekReportingPeriod),
        #     (FixedMonthFourthWeek, FixedMonthFourthWeekReportingPeriod),
        #     (FixedMonthFifthWeek, FixedMonthFifthWeekReportingPeriod)
        # ])
        # week_extrepperiod_matrix = OrderedDict([
        #     (FixedMonthFirstWeek, FixedMonthFirstWeekExtendedReportingPeriod),
        #     (FixedMonthSecondWeek,
        #      FixedMonthSecondWeekExtendedReportingPeriod),
        #     (FixedMonthThirdWeek, FixedMonthThirdWeekExtendedReportingPeriod),
        #     (FixedMonthFourthWeek,
        #      FixedMonthFourthWeekExtendedReportingPeriod),
        #     (FixedMonthFifthWeek, FixedMonthFifthWeekExtendedReportingPeriod)
        # ])

        # week_slug_matrix = OrderedDict([
        #     (FixedMonthFirstWeek,
        #      'malaria_weekly_epidemio_firstweek_aggregated'),
        #     (FixedMonthSecondWeek,
        #      'malaria_weekly_epidemio_secondweek_aggregated'),
        #     (FixedMonthThirdWeek,
        #      'malaria_weekly_epidemio_thirdweek_aggregated'),
        #     (FixedMonthFourthWeek,
        #      'malaria_weekly_epidemio_fourthweek_aggregated'),
        #     (FixedMonthFifthWeek,
        #      'malaria_weekly_epidemio_fifthweek_aggregated')
        # ])
        # for weekcls in week_slug_matrix.keys():
        #     logger.debug("\n\n-------")
        #     logger.debug(next_period)
        #     logger.debug(next_period.start_on)
        #     logger.debug(next_period.end_on)
        #     try:
        #         week_period = weekcls.find_create_from(
        #             year=next_period.start_on.year,
        #             month=next_period.start_on.month)
        #     except ValueError:
        #         continue
        #     if week_period is None:
        #         continue
        #     logger.debug(week_period)
        #     logger.debug(week_period.start_on)
        #     logger.debug(week_period.end_on)

        #     reporting_period = week_repperiod_matrix.get(weekcls) \
        #         .find_create_from(
        #             year=next_period.start_on.year,
        #             month=next_period.start_on.month)
        #     logger.debug(reporting_period)
        #     logger.debug(reporting_period.start_on)
        #     logger.debug(reporting_period.end_on)

        #     extended_reporting_period = week_extrepperiod_matrix \
        #         .get(weekcls).find_create_from(
        #             year=next_period.start_on.year,
        #             month=next_period.start_on.month)
        #     logger.debug(extended_reporting_period)
        #     logger.debug(extended_reporting_period.start_on)
        #     logger.debug(extended_reporting_period.end_on)

        #     reportcls_slug = week_slug_matrix.get(weekcls)
        #     logger.debug("ReportClass slug: {}".format(reportcls_slug))

        #     for entity in epidemio_cluster.members(only_active=True):

        #         edict = copy.copy(expected_dict)
        #         edict.update({
        #             'entity': entity,
        #             'period': week_period,
        #             'report_class': ReportClass.get_or_none(reportcls_slug),
        #             'reporting_period': reporting_period,
        #             'extended_reporting_period': extended_reporting_period,
        #         })
        #         e, created = ExpectedReporting.objects.get_or_create(**edict)
        #         if created:
        #             logger.debug("Created {}".format(e))
        #             created_list.append(e)
        #         else:
        #             logger.debug("Exists already: {}".format(e))

        ###
        # WEEKLY ROUTINE
        ###
        weekly_cluster = Cluster.get_or_none("malaria_weekly_routine")
        for day in range(1, nb_day_in_month + 1):
            day_period = DayPeriod.find_create_from(
                year=next_period.start_on.year,
                month=next_period.start_on.month, day=day)

            logger.debug("Generating DayPeriod Expecteds for {}"
                         .format(day_period))

            for entity in weekly_cluster.members(only_active=True):

                rcls = routinesrc_report_class \
                    if entity.type.slug == 'health_center' \
                    else routineagg_report_class
                edict = copy.copy(expected_dict)
                edict.update({
                    'entity': entity,
                    'period': day_period,
                    'report_class': rcls,
                    'reporting_period': None,
                    'extended_reporting_period': None,
                })
                e, created = ExpectedReporting.objects.get_or_create(**edict)
                if created:
                    logger.debug("Created {}".format(e))
                    created_list.append(e)
                else:
                    logger.debug("Exists already: {}".format(e))

        rcls2 = routineagg_week_report_class
        edict2 = copy.copy(expected_dict)
        edict2.update({
            'entity': entity,
            'period': day_period,
            'report_class': rcls2,
            'reporting_period': None,
            'extended_reporting_period': None,
        })
        e, created = ExpectedReporting.objects.get_or_create(**edict)
        if created:
            logger.debug("Created {}".format(e))
            created_list.append(e)
        else:
            logger.debug("Exists already: {}".format(e))

        # create FixedWeekPeriods for Epidemiology for the month
        week_repperiod_matrix = OrderedDict([
            (FixedMonthFirstWeek, FixedMonthFirstWeekReportingPeriod),
            (FixedMonthSecondWeek, FixedMonthSecondWeekReportingPeriod),
            (FixedMonthThirdWeek, FixedMonthThirdWeekReportingPeriod),
            (FixedMonthFourthWeek, FixedMonthFourthWeekReportingPeriod),
            (FixedMonthFifthWeek, FixedMonthFifthWeekReportingPeriod)
        ])
        week_extrepperiod_matrix = OrderedDict([
            (FixedMonthFirstWeek, FixedMonthFirstWeekExtendedReportingPeriod),
            (FixedMonthSecondWeek,
             FixedMonthSecondWeekExtendedReportingPeriod),
            (FixedMonthThirdWeek, FixedMonthThirdWeekExtendedReportingPeriod),
            (FixedMonthFourthWeek,
             FixedMonthFourthWeekExtendedReportingPeriod),
            (FixedMonthFifthWeek, FixedMonthFifthWeekExtendedReportingPeriod)
        ])

        week_slug_matrix = OrderedDict([
            (FixedMonthFirstWeek,
             'malaria_weekly_routine_firstweek_aggregated'),
            (FixedMonthSecondWeek,
             'malaria_weekly_routine_secondweek_aggregated'),
            (FixedMonthThirdWeek,
             'malaria_weekly_routine_thirdweek_aggregated'),
            (FixedMonthFourthWeek,
             'malaria_weekly_routine_fourthweek_aggregated'),
            (FixedMonthFifthWeek,
             'malaria_weekly_routine_fifthweek_aggregated')
        ])
        for weekcls in week_slug_matrix.keys():
            logger.debug("\n\n-------")
            logger.debug(next_period)
            logger.debug(next_period.start_on)
            logger.debug(next_period.end_on)
            try:
                week_period = weekcls.find_create_from(
                    year=next_period.start_on.year,
                    month=next_period.start_on.month)
            except ValueError:
                continue
            if week_period is None:
                continue
            logger.debug(week_period)
            logger.debug(week_period.start_on)
            logger.debug(week_period.end_on)

            reporting_period = week_repperiod_matrix.get(weekcls) \
                .find_create_from(
                    year=next_period.start_on.year,
                    month=next_period.start_on.month)
            logger.debug(reporting_period)
            logger.debug(reporting_period.start_on)
            logger.debug(reporting_period.end_on)

            extended_reporting_period = week_extrepperiod_matrix \
                .get(weekcls).find_create_from(
                    year=next_period.start_on.year,
                    month=next_period.start_on.month)
            logger.debug(extended_reporting_period)
            logger.debug(extended_reporting_period.start_on)
            logger.debug(extended_reporting_period.end_on)

            reportcls_slug = week_slug_matrix.get(weekcls)
            logger.debug("ReportClass slug: {}".format(reportcls_slug))

            for entity in weekly_cluster.members(only_active=True):

                edict = copy.copy(expected_dict)
                edict.update({
                    'entity': entity,
                    'period': week_period,
                    'report_class': ReportClass.get_or_none(reportcls_slug),
                    'reporting_period': reporting_period,
                    'extended_reporting_period': extended_reporting_period,
                })
                e, created = ExpectedReporting.objects.get_or_create(**edict)
                if created:
                    logger.debug("Created {}".format(e))
                    created_list.append(e)
                else:
                    logger.debug("Exists already: {}".format(e))

                reportcls_slug2 = reportcls_slug.replace(
                    '_aggregated', '_weeklong_aggregated')
                rc = ReportClass.get_or_none(reportcls_slug2)

                edict2 = copy.copy(expected_dict)
                edict2.update({
                    'entity': entity,
                    'period': week_period,
                    'report_class': ReportClass.get_or_none(reportcls_slug2),
                    'reporting_period': reporting_period,
                    'extended_reporting_period': extended_reporting_period,
                })
                e2, created2 = ExpectedReporting.objects \
                                                .get_or_create(**edict2)
                if created2:
                    logger.debug("Created {}".format(e2))
                    created_list.append(e2)
                else:
                    logger.debug("Exists already: {}".format(e2))

    return created_list


def report_classes_for(cluster):
    if cluster.slug == 'malaria_weekly_routine':
        return [routinesrc_report_class,
                routineagg_report_class,
                routineagg_week_report_class,
                # mwrfwa_report_class,
                # mwrswa_report_class,
                # mwrtwa_report_class,
                # mwrfowa_report_class,
                # mwrfiwa_report_class,
                mwrfwwa_report_class,
                mwrswwa_report_class,
                mwrtwwa_report_class,
                mwrfowwa_report_class,
                mwrfiwwa_report_class]
    return [indiv_report_class, agg_report_class]
