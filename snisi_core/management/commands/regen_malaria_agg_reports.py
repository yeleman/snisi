#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim: ai ts=4 sts=4 et sw=4 nu

from __future__ import (unicode_literals, absolute_import,
                        division, print_function)
import datetime
import logging

from django.core.management.base import BaseCommand
from django.utils import timezone
from optparse import make_option

from snisi_core.models.Reporting import (ExpectedReporting, SNISIReport,
                                         ExpectedValidation, ReportClass)
from snisi_core.models.Periods import MonthPeriod
from snisi_core.models.ValidationPeriods import DefaultRegionValidationPeriod
from snisi_core.models.Projects import Cluster
from snisi_core.models.Roles import Role
from snisi_core.models.Entities import Entity
from snisi_core.models.Providers import Provider
from snisi_malaria.models import AggMalariaR, MalariaR
from snisi_tools.datetime import DEBUG_change_system_date

logger = logging.getLogger(__name__)


class Command(BaseCommand):

    option_list = BaseCommand.option_list + (
        make_option('-c',
                    help='Clear Expected and Reports',
                    action='store_true',
                    default='',
                    dest='clear'),
    )

    def handle(self, *args, **options):

        autobot = Provider.get_or_none('autobot')
        reportcls_slug = "malaria_monthly_routine_aggregated"
        rclass = ReportClass.get_or_none(reportcls_slug)
        charge_sis = Role.get_or_none("charge_sis")
        first_period = MonthPeriod.from_url_str("09-2011")
        last_period = MonthPeriod.from_url_str("02-2014")
        first_period_mopti_district = MonthPeriod.from_url_str("09-2013")
        first_period_mopti_region = MonthPeriod.from_url_str("01-2014")
        mali = Entity.get_or_none("mali")

        def entity_expected_for(entity, period):
            if period > last_period:
                return False

            if entity is mali:
                return period >= first_period

            region = entity.get_health_region()

            if region.slug in ('9GR8', '2732'):
                return period >= first_period
            elif region.slug == 'SSH3':
                if entity.slug == 'HFD9':
                    return period >= first_period_mopti_district
                else:
                    return period >= first_period_mopti_region
            else:
                return False

        # remove old ones if requested
        if options.get('clear'):
            ExpectedReporting.objects.filter(report_class__slug=reportcls_slug).delete()
            receipts = [r.receipt for r in AggMalariaR.objects.all()]
            AggMalariaR.objects.filter(receipt__in=receipts)
            SNISIReport.objects.filter(receipt__in=receipts).delete()
            ExpectedValidation.objects.filter(report__receipt__in=receipts).delete()

        cluster = Cluster.get_or_none("malaria_monthly_routine")
        periods = MonthPeriod.all_from(first_period, last_period)
        districts = [e for e in cluster.members() if e.type.slug == 'health_district']
        regions = [e for e in cluster.members() if e.type.slug == 'health_region']

        # loop on periods
        for period in periods:

            logger.info("Switching to {}".format(period))

            region_validation_period = DefaultRegionValidationPeriod \
                                        .find_create_by_date(period.middle())

            # change date to beginning
            DEBUG_change_system_date(period.start_on, True)

            # loop on all districts/region/country
            for entity in districts + regions + [mali]:
                if not entity_expected_for(entity, period):
                    continue

                logger.info("\tCreating for {}".format(entity))

                # create expected reporting
                ExpectedReporting.objects.create(
                    report_class=rclass,
                    reporting_role=charge_sis if entity is not mali else None,
                    period=period,
                    within_period=False,
                    entity=entity,
                    within_entity=False,
                    amount_expected=ExpectedReporting.EXPECTED_SINGLE,
                    completion_status=ExpectedReporting.COMPLETION_MISSING)

            # change date to 16
            district_date = datetime.datetime(
                period.start_on.year,
                period.start_on.month,
                16, 8, 0).replace(tzinfo=timezone.utc)
            DEBUG_change_system_date(district_date, True)

            # loop on all districts
            for district in districts:
                if not entity_expected_for(district, period):
                    continue

                logger.info("\tAt district {}".format(district))

                # auto-validate non-validated reports
                for report in MalariaR.objects.filter(
                    period=period,
                    entity__in=district.get_health_centers()):
                    if not report.validated:
                        expv = ExpectedValidation.objects.get(report=report)

                        expv.acknowledge_validation(
                            validated=True,
                            validated_by=autobot,
                            validated_on=timezone.now(),
                            auto_validated=True)

                # create AggMalariaR
                agg = AggMalariaR.create_from(
                    period=period,
                    entity=district,
                    created_by=autobot)

                # ack expected
                exp = ExpectedReporting.objects.get(
                    report_class=rclass,
                    entity__slug=district.slug,
                    period=period)

                exp.acknowledge_report(agg)

                # create expected validation
                ExpectedValidation.objects.create(
                    report=agg,
                    validation_period=region_validation_period,
                    validating_entity=district.get_health_region(),
                    validating_role=charge_sis)

            # change date to 26
            region_date = datetime.datetime(
                period.start_on.year,
                period.start_on.month,
                26, 8, 0).replace(tzinfo=timezone.utc)
            DEBUG_change_system_date(region_date, True)

            # loop on all regions
            for region in regions:

                if not entity_expected_for(region, period):
                    continue

                logger.info("\tAt region {}".format(region))

                # loop on districts
                for district in [d for d in region.get_health_districts() if d in cluster.members()]:
                    if not entity_expected_for(district, period):
                        continue

                    logger.info("\t\tAt district {}".format(district))

                    # ack validation (auto)
                    expv = ExpectedValidation.objects.get(
                        report__entity=district,
                        report__period=period)

                    expv.acknowledge_validation(
                        validated=True,
                        validated_by=autobot,
                        validated_on=timezone.now(),
                        auto_validated=True)

                # create AggMalariaR/region
                agg = AggMalariaR.create_from(
                    period=period,
                    entity=region,
                    created_by=autobot)

                 # ack expected
                exp = ExpectedReporting.objects.get(
                    report_class=rclass,
                    entity__slug=region.slug,
                    period=period)

                exp.acknowledge_report(agg)

                # validate (no expected validation)
                agg.record_validation(
                    validated=True,
                    validated_by=autobot,
                    validated_on=timezone.now(),
                    auto_validated=True)

            # create AggMalariaR/country
            agg = AggMalariaR.create_from(
                period=period,
                entity=mali,
                created_by=autobot)

             # ack expected
            exp = ExpectedReporting.objects.get(
                report_class=rclass,
                entity__slug=mali.slug,
                period=period)

            exp.acknowledge_report(agg)

            # validate (no expected validation)
            agg.record_validation(
                validated=True,
                validated_by=autobot,
                validated_on=timezone.now(),
                auto_validated=True)

        DEBUG_change_system_date(None, True)