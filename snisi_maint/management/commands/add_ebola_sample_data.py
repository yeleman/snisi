#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim: ai ts=4 sts=4 et sw=4 nu

from __future__ import (unicode_literals, absolute_import,
                        division, print_function)
import logging
import datetime
import copy

from django.core.management.base import BaseCommand

from snisi_core.models.Reporting import (ExpectedReporting, ReportClass)
from snisi_core.models.Providers import Provider
from snisi_core.models.Entities import Entity
from snisi_core.models.Roles import Role
from snisi_core.models.Periods import MonthPeriod

from snisi_epidemiology.integrity import (EpidemiologyRIntegrityChecker,
                                          create_epid_report)
from snisi_epidemiology.models import EpidemiologyR, AggEpidemiologyR
from snisi_epidemiology.models import EpiWeekPeriod, EpiWeekReportingPeriod
from snisi_epidemiology.aggregations import generate_region_country_reports


logger = logging.getLogger(__name__)


class Command(BaseCommand):

    def handle(self, *args, **options):

        {
            #  13
            '01-04-2014': (1, 0),
            '02-04-2014': (1, 0),
            '03-04-2014': (1, 1),
            '04-04-2014': (1, 0),

            # 14
            '05-04-2014': (1, 0),
            '06-04-2014': (1, 0),

            # 15
            '17-04-2014': (1, 1),

            # 17
            '26-04-2014': (1, 1),

            # 19
            '08-05-2014': (1, 1),
            '09-05-2014': (1, 0),

            # 32
            '12-08-2014': (1, 0),
            '13-08-2014': (1, 0),

            # 35
            '03-09-2014': (1, 1),
            '04-09-2014': (1, 1),
            '05-09-2014': (1, 1),

            # 37
            '13-09-2014': (1, 0),
        }

        weeks_data = {
            'eW13-2014': (4, 1),
            'eW14-2014': (2, 0),
            'eW15-2014': (1, 1),
            'eW17-2014': (1, 1),
            'eW19-2014': (2, 1),
            'eW32-2014': (2, 0),
            'eW35-2014': (3, 3),
            'eW37-2014': (1, 0),

        }

        months_data = {
            '04-2014': (8, 3),
            '05-2014': (2, 1),
            '06-2014': (0, 0),
            '07-2014': (0, 0),
            '08-2014': (2, 0),
            '09-2014': (4, 3),
        }

        expected_dict = {
            'entity': Entity.get_or_none("mali"),
            'period': None,
            'within_period': False,
            'within_entity': False,
            'reporting_role': Role.get_or_none("charge_sis"),
            'reporting_period': None,
            'extended_reporting_period': None,
            'amount_expected': ExpectedReporting.EXPECTED_SINGLE
        }

        reportcls_epi = ReportClass.get_or_none(
            'epidemio_weekly_routine_aggregated')
        provider = Provider.get_or_none("autobot")

        start_week = EpiWeekPeriod.find_create_by_date(
            datetime.datetime(2014, 4, 1))
        end_week = EpiWeekPeriod.find_create_by_date(
            datetime.datetime(2014, 9, 20))
        weeks = EpiWeekPeriod.all_from(start_week, end_week)

        start_month = MonthPeriod.from_url_str("04-2014")
        end_month = MonthPeriod.from_url_str("09-2014")
        months = MonthPeriod.all_from(start_month, end_month)

        logger.info("Removing all ExpectedReporting...")
        ExpectedReporting.objects.filter(report_class=reportcls_epi).delete()
        logger.info("Removing all EpidemiologyR, AggEpidemiologyR...")
        EpidemiologyR.objects.all().delete()
        AggEpidemiologyR.objects.all().delete()

        def create_for(period, nb_cases, nb_deaths, periodcls=EpiWeekPeriod):
            checker = EpidemiologyRIntegrityChecker()
            checker.report_class = reportcls_epi
            checker.period_class = periodcls
            checker.set('year', period.end_on.year)
            checker.set('month', period.end_on.month)
            checker.set('day', period.end_on.day)

            for key in AggEpidemiologyR.data_fields():
                checker.set(key, 0)
            checker.set('ebola_case', suspected)
            checker.set('ebola_death', death)

            try:
                hc = provider.location
            except:
                hc = None

            checker.set('entity', hc)
            checker.set('hc', getattr(hc, 'slug', None))
            checker.set('submit_time',
                        period.end_on + datetime.timedelta(days=1))
            checker.set('author', provider.name())
            checker.set('submitter', provider)

            # test the data
            checker.check()
            if not checker.is_valid():
                error = checker.errors.pop().render(short=True)
                logger.debug("Error in data: {}".format(error))
                raise ValueError(error)

            # build requirements for report
            period = checker.get('period')
            entity = checker.get('entity')

            # expected reporting defines if report is expeted or not
            expected_reporting = ExpectedReporting.get_or_none(
                report_class=reportcls_epi,
                period=period,
                within_period=False,
                entity=entity,
                within_entity=False,
                amount_expected=ExpectedReporting.EXPECTED_SINGLE)

            report, text_message = create_epid_report(
                provider=provider,
                expected_reporting=expected_reporting,
                completed_on=period.end_on + datetime.timedelta(days=1),
                integrity_checker=checker,
                data_source="DNS data import",
                reportcls=AggEpidemiologyR)

            report.record_validation(
                validated=True,
                validated_by=provider,
                validated_on=None,
                auto_validated=True)

            logger.info(text_message)

        for week in weeks:
            logger.info(week)

            reporting_period = EpiWeekReportingPeriod.find_create_by_date(
                week.middle())

            # add ExpectedReporting for EpidemioAgg on Mali
            edict = copy.copy(expected_dict)
            edict.update({
                'period': week,
                'report_class': reportcls_epi,
                'reporting_period': reporting_period
            })

            expected = ExpectedReporting.objects.create(**edict)
            logger.info("Created Expected: {}".format(expected))

            # add report
            if not week.strid() in weeks_data.keys():
                continue

            suspected, death = weeks_data.get(week.strid())

            create_for(week, suspected, death)

            # report = AggEpidemiologyR(
            #     period=week,
            #     location=mali
            #     )
            # report.fill_blank()
            # report.ebola_case = suspected
            # report.ebola_death = death
            # report.save()

        logger.info("creating months")
        for month in months:
            sid = month.strid()
            logger.info("Switching to {}".format(month))

            # add ExpectedReporting for EpidemioAgg on Mali
            edict = copy.copy(expected_dict)
            edict.update({
                'period': month,
                'report_class': reportcls_epi,
                'reporting_period': month.following()
            })

            expected = ExpectedReporting.objects.create(**edict)
            logger.info("Created Expected: {}".format(expected))

            # add report
            if sid not in months_data.keys():
                continue

            suspected, death = months_data.get(sid)

            create_for(month, suspected, death, periodcls=MonthPeriod)
