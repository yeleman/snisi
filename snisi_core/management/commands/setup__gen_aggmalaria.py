#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim: ai ts=4 sts=4 et sw=4 nu

from __future__ import (unicode_literals, absolute_import,
                        division, print_function)
import datetime

from optparse import make_option
from django.core.management.base import BaseCommand
from django.utils import timezone

from snisi_core.models.Entities import HealthEntity
from snisi_core.models.Providers import Provider
from snisi_core.models.Roles import Role
from snisi_core.models.Reporting import ExpectedReporting, ExpectedValidation
from snisi_malaria.models import AggMalariaR
from snisi_tools.datetime import DEBUG_change_system_date
from snisi_core.models.ValidationPeriods import (
    DefaultDistrictValidationPeriod, DefaultRegionValidationPeriod,
    DefaultNationalValidationPeriod)


class Command(BaseCommand):

    option_list = BaseCommand.option_list + (
        make_option('-c',
                    help='Delete all MalariaR and AggMalariaR first',
                    action='store_true',
                    dest='clear'),
        )

    def handle(self, *args, **options):

        level_day = {
            'health_district': 16,
            'health_region': 26,
            'country': 27
        }

        print("Starting generation of AggMalariaR objects.")

        autobot = Provider.active.get(username='autobot')
        role_chargesis = Role.objects.get(slug='charge_sis')
        # jan = MonthPeriod.find_create_from(year=2014, month=1)

        if options.get('clear'):
            print("Removing AggMalariaR objects...")
            HealthEntity.objects.all().delete()

        for level in ('health_district', 'health_region', 'country'):

            print("Generating for {}".format(level))

            for exp in ExpectedReporting.objects.filter(
                    entity__type__slug=level,
                    report_class__slug='malaria_monthly_routine_aggregated'):

                # if level == 'country' and exp.period == jan:
                #     continue

                agg_date = datetime.datetime(
                    exp.period.following().middle().year,
                    exp.period.following().middle().month,
                    level_day.get(level), 8, 0).replace(tzinfo=timezone.utc)

                DEBUG_change_system_date(agg_date, True)

                agg_r = AggMalariaR.create_from(
                    entity=exp.entity,
                    period=exp.period,
                    created_by=autobot)

                exp.acknowledge_report(agg_r)

                valperiodcls = DefaultDistrictValidationPeriod \
                    if level == 'health_center' \
                    else DefaultRegionValidationPeriod
                if level == 'country':
                    valperiodcls = DefaultNationalValidationPeriod

                validating_entity = agg_r.entity \
                    if level == 'country' else agg_r.entity.parent
                validating_role = Role.objects.get(slug='validation_bot') \
                    if level == 'country' else role_chargesis
                exv = ExpectedValidation.objects.create(
                    report=agg_r,
                    validation_period=valperiodcls.find_create_by_date(
                        agg_r.period.middle()),
                    validating_entity=validating_entity,
                    validating_role=validating_role,
                )

                exv.acknowledge_validation(validated=True,
                                           validated_by=autobot,
                                           validated_on=agg_date,
                                           auto_validated=True)
