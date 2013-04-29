#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim: ai ts=4 sts=4 et sw=4 nu

from __future__ import (unicode_literals, absolute_import,
                        division, print_function)
import logging
import datetime
from optparse import make_option

from django.core.management.base import BaseCommand

from snisi_tools.datetime import DEBUG_change_system_date
from snisi_core.models.Entities import Entity
from snisi_core.models.Reporting import (get_autobot, ExpectedReporting,
                                         ReportClass, PERIODICAL_AGGREGATED)
from snisi_core.models.Periods import DayPeriod, MonthPeriod
from snisi_malaria.models import (EpidemioMalariaR,
                                  DailyMalariaR, AggDailyMalariaR,
                                  AggWeeklyMalariaR)
from snisi_core.models.FixedWeekPeriods import (FixedMonthFirstWeek,
                                                FixedMonthSecondWeek,
                                                FixedMonthThirdWeek,
                                                FixedMonthFourthWeek,
                                                FixedMonthFifthWeek)

logger = logging.getLogger(__name__)
mali = Entity.get_or_none("mali")
rsmopti = Entity.get_or_none("SSH3")
dsbandiagara = Entity.get_or_none("MJ86")
bandiagara = Entity.get_or_none("3ZF3")
dsmopti = Entity.get_or_none("HFD9")
ascotamb = Entity.get_or_none("ACE3")
sevare2 = Entity.get_or_none("KTE4")
autobot = get_autobot()
agg_locations = [dsmopti, dsbandiagara, rsmopti, mali]
week_agg_locations = [bandiagara, ascotamb, sevare2] + agg_locations
nbal = len(agg_locations)
period_classes = [
    FixedMonthFirstWeek,
    FixedMonthSecondWeek,
    FixedMonthThirdWeek,
    FixedMonthFourthWeek,
    FixedMonthFifthWeek,
]


class Command(BaseCommand):

    option_list = BaseCommand.option_list + (
        make_option('-c',
                    help='clear',
                    action='store_true',
                    dest='clear'),
        )

    def clear_all_data(self):
        logger.info("Clear all DailyMalariaR and AggDailyMalariaR...")
        DailyMalariaR.objects.all().delete()
        AggDailyMalariaR.objects.all().delete()
        logger.info("\tdone.")

    def create_all_dayreport(self):
        # Export all EpidemioMalariaR into DailyMalariaR
        logger.info("Generate DailyMalariaR for EpidemioMalariaR...")

        for exp in ExpectedReporting.objects.filter(
                report_class__slug__startswith='malaria_weekly_epidemio') \
                .order_by('period__start_on'):

            exp_data = exp.to_dict()
            exp_data['report_class'] = ReportClass.get_or_none(
                exp.report_class.slug.replace(
                    'malaria_weekly_epidemio',
                    'malaria_weekly_routine'))
            del(exp_data['completion_status'])
            new_exp = ExpectedReporting.objects.create(**exp_data)

            # Agg will be regenerated completely
            if not exp.entity.type.slug == 'health_center':
                continue

            # Weekly and Monthly Agg for location
            if exp.report_class.report_type == PERIODICAL_AGGREGATED:
                continue

            if exp.satisfied:
                epi_report = exp.arrived_report()
                logger.debug("\tFound report {} -- {} -- {}".format(
                    epi_report, epi_report.period, epi_report.created_on))
                data = {}
                for field in EpidemioMalariaR.meta_fields():
                    if field in ('receipt', 'report_cls', 'uuid'):
                        continue
                    data.update({field: epi_report.get(field)})

                data.update({
                    'u5_total_confirmed_malaria_cases':
                        epi_report.u5_total_confirmed_malaria_cases,
                    'o5_total_confirmed_malaria_cases':
                        epi_report.o5_total_confirmed_malaria_cases,
                    'pw_total_confirmed_malaria_cases':
                        epi_report.pw_total_confirmed_malaria_cases})

                # need to change system date so that receipt use proper
                # date elements (otherwise duplicates!)
                logger.debug("\tchange date to {}".format(
                    epi_report.created_on))
                DEBUG_change_system_date(epi_report.created_on, True)
                daily_report = DailyMalariaR.objects.create(**data)
                logger.info("Created {}".format(daily_report))

                new_exp.acknowledge_report(daily_report)
            else:
                epi_report = None

        logger.info("\tdone.")

    def gen_all_dayagg(self):

        logger.info("Generate AggDailyMalariaR for all DayPeriod")
        ps = DayPeriod.all_from(DailyMalariaR.objects.all().first().period,
                                DailyMalariaR.objects.all().last().period)

        for period in ps:

            # skip if period is complete
            if AggDailyMalariaR.objects.filter(period=period).count() == nbal:
                continue

            gen_time = period.end_on + \
                datetime.timedelta(seconds=28800)  # 8h

            DEBUG_change_system_date(gen_time, True)

            for entity in agg_locations:
                # skip if report exists
                if AggDailyMalariaR.objects.filter(period=period,
                                                   entity=entity).count():
                    continue

                agg_report = AggDailyMalariaR.create_from(
                    period=period,
                    entity=entity,
                    created_by=autobot)
                logger.info("Created {}".format(agg_report))

    def gen_all_weekagg(self):

        logger.info("Generate AggWeeklyMalariaR")

        for month_period in MonthPeriod.all_from(
                DailyMalariaR.objects.all().first().period,
                DailyMalariaR.objects.all().last().period):

            # loop on fixed weeks and try to find a period and report
            for periodcls in period_classes:
                period = periodcls.find_create_from(
                    month_period.middle().year, month_period.middle().month)

                if period is None:
                    continue

                # skip if period is complete
                if AggWeeklyMalariaR.objects.filter(
                        period=period).count() == nbal:
                    continue

                gen_time = period.end_on + \
                    datetime.timedelta(seconds=28800)  # 8h

                DEBUG_change_system_date(gen_time, True)

                for entity in week_agg_locations:
                    # skip if report exists
                    if AggWeeklyMalariaR.objects.filter(period=period,
                                                        entity=entity).count():
                        continue

                    agg_report = AggWeeklyMalariaR.create_from(
                        period=period,
                        entity=entity,
                        created_by=autobot)
                    logger.info("Created {}".format(agg_report))

    def handle(self, *args, **options):

        if options.get('clear'):
            self.clear_all_data()

        nb_old = ExpectedReporting.objects.filter(
            report_class__slug__startswith='malaria_weekly_epidemio').count()
        nb_new = ExpectedReporting.objects.filter(
            report_class__slug__startswith='malaria_weekly_routine').count()

        # uncomplete first stage ; remove everything
        if nb_old != nb_new:
            self.clear_all_data()

        # first stage not processed ; process
        if nb_new == 0:
            self.create_all_dayreport()

        # generate AggDailyMalariaR
        # self.gen_all_weekagg()

        # generate AggWeeklyMalariaR
        self.gen_all_weekagg()

        logger.info("All done.")
