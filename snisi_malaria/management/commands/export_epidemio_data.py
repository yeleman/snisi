#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim: ai ts=4 sts=4 et sw=4 nu

from __future__ import (unicode_literals, absolute_import,
                        division, print_function)
import logging
import datetime

from django.core.management.base import BaseCommand

from snisi_tools.datetime import DEBUG_change_system_date
from snisi_core.models.Entities import Entity
from snisi_core.models.Reporting import (get_autobot, ExpectedReporting,
                                         ReportClass, PERIODICAL_AGGREGATED)
from snisi_core.models.Periods import DayPeriod
from snisi_malaria.models import (EpidemioMalariaR,
                                  WeeklyMalariaR, AggWeeklyMalariaR)

logger = logging.getLogger(__name__)


class Command(BaseCommand):

    def handle(self, *args, **options):

        mali = Entity.get_or_none("mali")
        rsmopti = Entity.get_or_none("SSH3")
        dsbandiagara = Entity.get_or_none("MJ86")
        dsmopti = Entity.get_or_none("HFD9")
        autobot = get_autobot()

        logger.info("Clear all WeeklyMalariaR and AggWeeklyMalariaR...")
        WeeklyMalariaR.objects.all().delete()
        AggWeeklyMalariaR.objects.all().delete()
        logger.info("\tdone.")

        # Export all EpidemioMalariaR into WeeklyMalariaR
        logger.info("Generate WeeklyMalariaR for EpidemioMalariaR...")

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
                weekly_report = WeeklyMalariaR.objects.create(**data)
                logger.info("Created {}".format(weekly_report))

                new_exp.acknowledge_report(weekly_report)
            else:
                epi_report = None

        logger.info("\tdone.")


        ## need to handle AggWeek (and AggMonth ?)

        logger.info("Generate AggWeeklyMalariaR for all DayPeriod")

        ps = DayPeriod.all_from(WeeklyMalariaR.objects.all().first().period,
                                WeeklyMalariaR.objects.all().last().period)

        for period in ps:
            gen_time = epi_report.extended_reporting_period.end_on + \
                datetime.timedelta(seconds=28800)  # 8h
            DEBUG_change_system_date(gen_time, True)
            for entity in [dsmopti, dsbandiagara, rsmopti, mali]:
                agg_report = AggWeeklyMalariaR.create_from(
                    period=period,
                    entity=entity,
                    created_by=autobot)
                logger.info("Created {}".format(agg_report))

        logger.info("All done.")
