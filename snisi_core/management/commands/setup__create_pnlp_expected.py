#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim: ai ts=4 sts=4 et sw=4 nu

from __future__ import (unicode_literals, absolute_import,
                        division, print_function)
import json

from optparse import make_option
from django.core.management.base import BaseCommand

from snisi_core.models.Entities import HealthEntity, Entity
from snisi_core.models.Reporting import ExpectedReporting, ReportClass
from snisi_core.models.Periods import MonthPeriod
from snisi_core.models.Roles import Role
from snisi_core.models.ReportingPeriods import (
    DefaultMonthlyReportingPeriod, DefaultMonthlyExtendedReportingPeriod)
from snisi_tools.datetime import DEBUG_change_system_date


class Command(BaseCommand):

    option_list = BaseCommand.option_list + (
        make_option('-f',
                    help='JSON matrix of old and new codes',
                    action='store',
                    dest='input_file'),
        make_option('-c',
                    help='Delete all ExpectedReporting first',
                    action='store_true',
                    dest='clear'),
        make_option('-y',
                    help='Year to prodice expected for',
                    action='store',
                    dest='year')
        )

    def handle(self, *args, **options):

        input_file = open(options.get('input_file'), 'r')
        matrix = json.load(input_file)

        dtc = Role.objects.get(slug='dtc')
        chargesis = Role.objects.get(slug='charge_sis')

        year = int(options.get('year'))

        if options.get('clear'):
            print("Removing all expected...")
            ExpectedReporting.objects.all().delete()

        print("Creating ExpectedReporting...")

        report_source = ReportClass.objects.get(slug='malaria_monthly_routine')
        report_agg = ReportClass.objects.get(slug='malaria_monthly_routine_aggregated')

        # create periods
        print("Creating Periods")
        if year == 2011:
            smonth = 7
        else:
            smonth = 1
        if year == 2014:
            emonth = 1
        else:
            emonth = 12

        # 2012 is splitted
        if year == 20121:
            year = 2012
            smonth = 1
            emonth = 6
        elif year == 20122:
            year = 2012
            smonth = 7
            emonth = 12

        # 2013 is splitted
        if year == 20131:
            year = 2013
            smonth = 1
            emonth = 6
        elif year == 20132:
            year = 2013
            smonth = 7
            emonth = 12

        if year == 2014:
            smonth = 1
            emonth = 2

        print(year)
        period = MonthPeriod.find_create_from(year=year, month=smonth)
        end = MonthPeriod.find_create_from(year=year, month=emonth)
        periods = []
        while period < end:
            periods.append(period)
            period = period.following()
        periods.append(end)

        mopti = Entity.get_or_none("SSH3")
        moptid = Entity.get_or_none("HFD9")

        september13 = MonthPeriod.find_create_from(year=2013, month=9)
        january14 = MonthPeriod.find_create_from(year=2014, month=1)

        for period in periods:

            # Change date to Period start
            DEBUG_change_system_date(period.start_on, True)

            for new, old in matrix['new_old'].items():
                print(new)
                entity = Entity.get_or_none(new)
                print(entity)

                if not entity.type.slug == 'health_center':
                    # no reporting period for Agg.
                    reporting_period = None
                    extended_reporting_period = None

                if entity.type.slug == 'health_center':
                    reporting_period = DefaultMonthlyReportingPeriod.find_create_by_date(period.following().middle())
                    extended_reporting_period = DefaultMonthlyExtendedReportingPeriod.find_create_by_date(period.following().middle())
                else:
                    # no reporting period for Agg.
                    reporting_period = None
                    extended_reporting_period = None

                reportcls = report_source if entity.type.slug == 'health_center' else report_agg
                role = dtc if entity.type.slug == 'health_center' else chargesis

                if entity in mopti.get_health_descendants() and period < september13:
                    continue
                if entity in moptid.get_health_descendants() and period < january14:
                    continue

                e = ExpectedReporting.objects.create(
                    report_class=reportcls,
                    period=period,
                    within_period=False,
                    entity=entity,
                    within_entity=False,
                    reporting_role=role,
                    reporting_period=reporting_period,
                    extended_reporting_period=extended_reporting_period,
                    amount_expected=ExpectedReporting.EXPECTED_SINGLE)

                del(reporting_period)
                del(extended_reporting_period)
                del(reportcls)
                del(role)
                del(entity)
                del(e)
                del(new)

