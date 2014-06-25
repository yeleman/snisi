#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim: ai ts=4 sts=4 et sw=4 nu

from __future__ import (unicode_literals, absolute_import,
                        division, print_function)
import logging

from django.utils import timezone

from snisi_core.models.Reporting import (ExpectedReporting,
                                         ExpectedValidation, ReportClass)
from snisi_core.models.ValidationPeriods import DefaultRegionValidationPeriod
from snisi_core.models.Projects import Cluster
from snisi_core.models.Roles import Role
from snisi_core.models.Entities import Entity
from snisi_core.models.Providers import Provider
from snisi_vacc.models import AggVaccCovR, VaccCovR
from snisi_vacc import (ROUTINE_DISTRICT_AGG_DAY,
                        ROUTINE_REGION_AGG_DAY)
from snisi_tools.misc import class_str

logger = logging.getLogger(__name__)

autobot = Provider.get_or_none('autobot')
reportcls_slug = "major_vaccine_monthly_aggregated"
rclass = ReportClass.get_or_none(reportcls_slug)
charge_sis = Role.get_or_none("charge_sis")

mali = Entity.get_or_none("mali")
cluster = Cluster.get_or_none("vacc_coverage_routine")

get_districts = lambda: [e for e in cluster.members()
                         if e.type.slug == 'health_district']
get_regions = lambda: [e for e in cluster.members()
                       if e.type.slug == 'health_region']


def generate_district_reports(period,
                              ensure_correct_date=True):

    logger.info("Switching to {}".format(period))

    region_validation_period = DefaultRegionValidationPeriod \
                                .find_create_by_date(period.middle())

    if ensure_correct_date:
        now = timezone.now()
        if not period.following().includes(now) \
         or not now.day == ROUTINE_DISTRICT_AGG_DAY:
            logger.error("Not allowed to generate district agg "
                         "outside the 11th of the following period")
            return

    districts = get_districts()

    # loop on all districts
    for district in districts:

        # ack expected
        exp = ExpectedReporting.objects.filter(
            report_class=rclass,
            entity__slug=district.slug,
            period=period)

        # not expected
        if exp.count() == 0:
            continue
        else:
            # might explode if 2 exp but that's the point
            exp = exp.get()

        logger.info("\tAt district {}".format(district))

        # auto-validate non-validated reports
        for report in VaccCovR.objects.filter(
            period=period,
            entity__in=district.get_health_centers()):
            if not report.validated:
                expv = ExpectedValidation.objects.get(report=report)

                expv.acknowledge_validation(
                    validated=True,
                    validated_by=autobot,
                    validated_on=timezone.now(),
                    auto_validated=True)

        # create AggVaccCovR
        agg = AggVaccCovR.create_from(
            period=period,
            entity=district,
            created_by=autobot)

        exp.acknowledge_report(agg)

        # create expected validation
        ExpectedValidation.objects.create(
            report=agg,
            validation_period=region_validation_period,
            validating_entity=district.get_health_region(),
            validating_role=charge_sis)


def generate_region_country_reports(period,
                                    ensure_correct_date=True):

    logger.info("Switching to {}".format(period))

    if ensure_correct_date:
        now = timezone.now()
        if not period.following().includes(now) \
         or not now.day == ROUTINE_REGION_AGG_DAY:
            logger.error("Not allowed to generate district agg "
                         "outside the 11th of the following period")
            return

    regions = get_regions()

    # loop on all regions
    for region in regions:

        # ack expected
        exp = ExpectedReporting.objects.filter(
            report_class=rclass,
            entity__slug=region.slug,
            period=period)

        if exp.count() == 0:
            continue
        else:
            exp = exp.get()

        logger.info("\tAt region {}".format(region))

        # loop on districts
        for district in [d for d in region.get_health_districts()
                         if d in cluster.members()]:

            logger.info("\t\tAt district {}".format(district))

            try:
                # ack validation (auto)
                expv = ExpectedValidation.objects.get(
                    report__entity=district,
                    report__period=period,
                    report__report_cls=class_str(VaccCovR))
            except ExpectedValidation.DoesNotExist:
                continue

            expv.acknowledge_validation(
                validated=True,
                validated_by=autobot,
                validated_on=timezone.now(),
                auto_validated=True)

        # create AggVaccCovR/region
        agg = AggVaccCovR.create_from(
            period=period,
            entity=region,
            created_by=autobot)

        exp.acknowledge_report(agg)

        # validate (no expected validation)
        agg.record_validation(
            validated=True,
            validated_by=autobot,
            validated_on=timezone.now(),
            auto_validated=True)

    # ack expected
    exp = ExpectedReporting.objects.get(
        report_class=rclass,
        entity__slug=mali.slug,
        period=period)

    if exp is None:
        return

    # create AggVaccCovR/country
    agg = AggVaccCovR.create_from(
        period=period,
        entity=mali,
        created_by=autobot)

    exp.acknowledge_report(agg)

    # validate (no expected validation)
    agg.record_validation(
        validated=True,
        validated_by=autobot,
        validated_on=timezone.now(),
        auto_validated=True)
