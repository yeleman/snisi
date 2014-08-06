#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim: ai ts=4 sts=4 et sw=4 nu

from __future__ import (unicode_literals, absolute_import,
                        division, print_function)
import logging
from datetime import timedelta

from django.core.management.base import BaseCommand
from django.utils import timezone

from snisi_core.models.Periods import MonthPeriod, DayPeriod
from snisi_core.models.Reporting import ExpectedReporting
from snisi_core.models.Entities import Entity
from snisi_core.models.Providers import Provider
from snisi_tools.datetime import DEBUG_change_system_date
from snisi_malaria.models import MalariaR, EpidemioMalariaR

logger = logging.getLogger(__name__)


class Command(BaseCommand):

    def handle(self, *args, **options):

        speriod = MonthPeriod.from_url_str("01-2013")
        eperiod = MonthPeriod.from_url_str("12-2013")
        periods = MonthPeriod.all_from(speriod, eperiod)

        autobot = Provider.get_or_none("autobot")

        for period in periods:

            for entity_slug in ['ACE3', 'KTE4', '3ZF3']:

                entity = Entity.get_or_none(entity_slug)

                if entity_slug == 'ACE3' and period.middle().month >= 10:
                    continue

                if entity_slug == 'KTE4' and period.middle().month >= 9:
                    continue

                day_periods = DayPeriod.objects.filter(
                    start_on__gte=period.start_on,
                    end_on__lte=period.end_on)
                day_reports = EpidemioMalariaR.objects.filter(
                    period__in=day_periods,
                    entity=entity)

                # change date to begining of period
                DEBUG_change_system_date(period.start_on, True)

                # create expected if not exist
                eo = ExpectedReporting.objects.get(
                    period=period, entity__slug='S5C4')
                expected_reporting = eo.clone(
                    save=True,
                    entity=entity,
                    completion_status=ExpectedReporting.COMPLETION_MISSING)

                DEBUG_change_system_date(
                    period.start_on + timedelta(days=1), True)

                provider = Provider.objects.get(
                    location=entity, role__slug='dtc')
                report = MalariaR.start(
                    period=period,
                    entity=entity,
                    created_by=provider,
                    arrival_status=MalariaR.ON_TIME)

                def sum_days(fields):
                    fields = [fields] \
                        if not isinstance(fields, (tuple, list)) else fields
                    return sum([sum([getattr(r, field, 0)
                                for r in day_reports for field in fields])])

                report.fill_blank()

                report.add_underfive_data(
                    total_consultation_all_causes=sum_days(
                        'u5_total_consultation_all_causes'),
                    total_suspected_malaria_cases=sum_days(
                        'u5_total_suspected_malaria_cases'),
                    total_simple_malaria_cases=sum_days(
                        'u5_total_simple_malaria_cases'),
                    total_severe_malaria_cases=sum_days(
                        'u5_total_severe_malaria_cases'),
                    total_tested_malaria_cases=sum_days(
                        ['u5_total_rdt_tested_malaria_cases',
                         'u5_total_ts_tested_malaria_cases']),
                    total_confirmed_malaria_cases=sum_days(
                        ['u5_total_rdt_confirmed_malaria_cases',
                         'u5_total_ts_confirmed_malaria_cases']),
                    total_treated_malaria_cases=0,
                    total_inpatient_all_causes=0,
                    total_malaria_inpatient=0,
                    total_death_all_causes=sum_days(
                        'u5_total_death_all_causes'),
                    total_malaria_death=sum_days(
                        'u5_total_malaria_death'),
                    total_distributed_bednets=0)
                report.add_overfive_data(
                    total_consultation_all_causes=sum_days(
                        'o5_total_consultation_all_causes'),
                    total_suspected_malaria_cases=sum_days(
                        'o5_total_suspected_malaria_cases'),
                    total_simple_malaria_cases=sum_days(
                        'o5_total_simple_malaria_cases'),
                    total_severe_malaria_cases=sum_days(
                        'o5_total_severe_malaria_cases'),
                    total_tested_malaria_cases=sum_days(
                        ['o5_total_rdt_tested_malaria_cases',
                         'o5_total_ts_tested_malaria_cases']),
                    total_confirmed_malaria_cases=sum_days(
                        ['o5_total_rdt_confirmed_malaria_cases',
                         'o5_total_ts_confirmed_malaria_cases']),
                    total_treated_malaria_cases=0,
                    total_inpatient_all_causes=0,
                    total_malaria_inpatient=0,
                    total_death_all_causes=sum_days(
                        'o5_total_death_all_causes'),
                    total_malaria_death=sum_days(
                        'o5_total_malaria_death'))
                report.add_pregnantwomen_data(
                    total_consultation_all_causes=sum_days(
                        'pw_total_consultation_all_causes'),
                    total_suspected_malaria_cases=sum_days(
                        'pw_total_suspected_malaria_cases'),
                    total_severe_malaria_cases=sum_days(
                        'pw_total_severe_malaria_cases'),
                    total_tested_malaria_cases=sum_days(
                        ['pw_total_rdt_tested_malaria_cases',
                         'pw_total_ts_tested_malaria_cases']),
                    total_confirmed_malaria_cases=sum_days(
                        ['pw_total_rdt_confirmed_malaria_cases',
                         'pw_total_ts_confirmed_malaria_cases']),
                    total_treated_malaria_cases=0,
                    total_inpatient_all_causes=0,
                    total_malaria_inpatient=0,
                    total_death_all_causes=sum_days(
                        'pw_total_death_all_causes'),
                    total_malaria_death=sum_days(
                        'pw_total_malaria_death'),
                    total_distributed_bednets=0,
                    total_anc1=0,
                    total_sp1=0,
                    total_sp2=0)

                # create MalariaR source report from AggEpi
                report.save()
                logger.info(report)

                expected_reporting.acknowledge_report(report)

                report.record_validation(validated=True,
                                         validated_by=autobot,
                                         validated_on=timezone.now(),
                                         auto_validated=True)

        DEBUG_change_system_date(None, True)
