#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim: ai ts=4 sts=4 et sw=4 nu

from __future__ import (unicode_literals, absolute_import,
                        division, print_function)
import logging
import datetime

from django.utils import timezone

from snisi_core.models.Reporting import (ExpectedReporting,
                                         ExpectedValidation, ReportClass)
from snisi_core.models.ValidationPeriods import DefaultRegionValidationPeriod
from snisi_core.models.Projects import Cluster
from snisi_core.models.Roles import Role
from snisi_core.models.Entities import Entity
from snisi_core.models.Providers import Provider
from snisi_nutrition.models.Monthly import AggNutritionR
from snisi_nutrition.models.Weekly import (
    NutWeekRegionValidationPeriod, AggWeeklyNutritionR)
from snisi_nutrition import (ROUTINE_DISTRICT_AGG_DAY,
                             ROUTINE_REGION_AGG_DAY,
                             ROUTINE_DISTRICT_AGG_DAYS_DELTA,
                             ROUTINE_REGION_AGG_DAYS_DELTA)
from snisi_nutrition.integrity import PROJECT_BRAND
from snisi_core.models.Notifications import Notification

logger = logging.getLogger(__name__)

autobot = Provider.get_or_none('autobot')
reportcls_slug = "nutrition_monthly_routine_aggregated"
rclass = ReportClass.get_or_none(reportcls_slug)
charge_sis = Role.get_or_none("charge_sis")

mali = Entity.get_or_none("mali")
cluster = Cluster.get_or_none("nutrition_routine")

get_districts = lambda: [e for e in cluster.members()
                         if e.type.slug == 'health_district']
get_regions = lambda: [e for e in cluster.members()
                       if e.type.slug == 'health_region']


def handle_district_validation(district,
                               report_class, report_class_agg,
                               period, region_validation_period):

    report_cls = report_class.report_class
    report_cls_agg = report_class_agg.report_class

    # find expected for Agg
    exp = ExpectedReporting.objects.filter(
        report_class=report_class_agg,
        entity__slug=district.slug,
        period=period)

    # not expected
    if exp.count() == 0:
        return None, None, None
    else:
        # might explode if 2 exp but that's the point
        exp = exp.get()

    # auto-validate non-validated reports
    for report in report_cls.objects.filter(
            period=period, entity__in=district.get_health_centers()):
        if not report.validated:
            expv = ExpectedValidation.objects.get(report=report)

            expv.acknowledge_validation(
                validated=True,
                validated_by=autobot,
                validated_on=timezone.now(),
                auto_validated=True)

    # create Aggregated Report
    agg = report_cls_agg.create_from(
        period=period,
        entity=district,
        created_by=autobot)

    exp.acknowledge_report(agg)

    # create expected validation
    expv = ExpectedValidation.objects.create(
        report=agg,
        validation_period=region_validation_period,
        validating_entity=district.get_health_region(),
        validating_role=charge_sis)

    return exp, agg, expv


def handle_region_validation(region, report_class_agg, period):

    report_cls_agg = report_class_agg.report_class

    # get Expected Agg
    exp = ExpectedReporting.objects.filter(
        report_class=report_class_agg,
        entity__slug=region.slug,
        period=period)

    if exp.count() == 0:
        return None, None
    else:
        exp = exp.get()

    # loop on districts
    for district in [d for d in region.get_health_districts()
                     if d in cluster.members()]:

        logger.info("\t\tAt district {}".format(district))

        try:
            # ack validation (auto)
            expv = ExpectedValidation.objects.get(
                report__report_cls=report_class_agg.cls,
                report__entity=district,
                report__period=period)
        except ExpectedValidation.DoesNotExist:
            continue

        expv.acknowledge_validation(
            validated=True,
            validated_by=autobot,
            validated_on=timezone.now(),
            auto_validated=True)

    # create Agg/region
    agg = report_cls_agg.create_from(
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

    return exp, agg


def handle_country_validation(country, report_class_agg, period):

    report_cls_agg = report_class_agg.report_class

    # ack expected
    exp = ExpectedReporting.objects.get(
        report_class=report_class_agg,
        entity=country,
        period=period)

    if exp is None:
        return None, None

    # create AggNutritionR/country
    agg = report_cls_agg.create_from(
        period=period,
        entity=country,
        created_by=autobot)

    exp.acknowledge_report(agg)

    # validate (no expected validation)
    agg.record_validation(
        validated=True,
        validated_by=autobot,
        validated_on=timezone.now(),
        auto_validated=True)

    return exp, agg


def generate_weekly_district_reports(period, ensure_correct_date=True):

    logger.debug("generate_weekly_district_reports {}".format(period))

    logger.info("Switching to {}".format(period))

    region_validation_period = NutWeekRegionValidationPeriod \
        .find_create_by_date(period.middle())

    if ensure_correct_date:
        now = timezone.now()
        district_agg_day = period.end_on + datetime.timedelta(
            days=ROUTINE_DISTRICT_AGG_DAYS_DELTA)
        if not now.date() == district_agg_day.date():
            logger.error("Not allowed to generate district agg "
                         "outside the next Sunday")
            return False

    logger.debug("OK to process district reports")

    districts = get_districts()

    # loop on all districts
    for district in districts:

        # skip if exists (assume if AggNutritionR exist, all others exist too)
        if AggWeeklyNutritionR.objects.filter(
                period=period, entity=district).count():
            continue

        logger.info("\tAt district {}".format(district))

        # AggWeeklyNutritionR
        nut_exp, nut_agg, nut_expv = handle_district_validation(
            district=district,
            report_class=ReportClass.get_or_none("nutrition_weekly_routine"),
            report_class_agg=ReportClass.get_or_none(
                "nutrition_weekly_routine_aggregated"),
            period=period,
            region_validation_period=region_validation_period)

        # send notification to Region
        for recipient in Provider.active.filter(
                role=charge_sis, location=nut_agg.entity.get_health_region()):

            Notification.create(
                provider=recipient,
                deliver=Notification.TODAY,
                expirate_on=region_validation_period.end_on,
                category=PROJECT_BRAND,
                text="Le rapport (aggrégé) de routine Nutrition hedomadaire "
                     "de {period} pour {entity} est prêt. "
                     "No reçu: #{receipt}. "
                     "Vous devez le valider avant le 25."
                     .format(entity=nut_agg.entity.display_full_name(),
                             period=nut_agg.period,
                             receipt=nut_agg.receipt)
                )


def generate_weekly_region_country_reports(period, ensure_correct_date=True):

    logger.debug("generate_weekly_region_country_reports {}".format(period))

    logger.info("Switching to {}".format(period))

    if ensure_correct_date:
        now = timezone.now()
        region_agg_day = period.end_on + datetime.timedelta(
            days=ROUTINE_REGION_AGG_DAYS_DELTA)
        if not now.date() == region_agg_day.date():
            logger.error("Not allowed to generate district agg "
                         "outside the next Monday")
            return False

    regions = get_regions()

    # loop on all regions
    for region in regions:

        logger.info("\tAt region {}".format(region))

        # AggWeeklyNutritionR
        nut_exp, nut_agg = handle_region_validation(
            region=region,
            report_class_agg=ReportClass.get_or_none(
                "nutrition_weekly_routine_aggregated"),
            period=period)

    # COUNTRY LEVEL
    country = mali

    logger.info("\tAt {}".format(mali))

    # AggWeeklyNutritionR
    nut_exp, nut_agg = handle_country_validation(
        country=country,
        report_class_agg=ReportClass.get_or_none(
            "nutrition_weekly_routine_aggregated"),
        period=period)

    # send notification to National level
    for recipient in Provider.active.filter(location__level=0):

        Notification.create(
            provider=recipient,
            deliver=Notification.TODAY,
            expirate_on=nut_agg.period.following().following().start_on,
            category=PROJECT_BRAND,
            text="Le rapport national (aggrégé) de routine Nutrition hedbo. "
                 "pour {period} est disponible. No reçu: #{receipt}."
                 .format(period=nut_agg.period, receipt=nut_agg.receipt))


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
                         "outside the 16th of the following period")
            return False

    districts = get_districts()

    # loop on all districts
    for district in districts:

        # skip if exists (assume if AggNutritionR exist, all others exist too)
        if AggNutritionR.objects.filter(
                period=period, entity=district).count():
            continue

        logger.info("\tAt district {}".format(district))

        # URENAM
        urenam_exp, urenam_agg, urenam_expv = handle_district_validation(
            district=district,
            report_class=ReportClass.get_or_none("nut_urenam_monthly_routine"),
            report_class_agg=ReportClass.get_or_none(
                "nut_urenam_monthly_routine_aggregated"),
            period=period,
            region_validation_period=region_validation_period)
        logger.info("\t\tsub-report: {}".format(urenam_agg))

        # URENAS
        urenas_exp, urenas_agg, urenas_expv = handle_district_validation(
            district=district,
            report_class=ReportClass.get_or_none("nut_urenas_monthly_routine"),
            report_class_agg=ReportClass.get_or_none(
                "nut_urenas_monthly_routine_aggregated"),
            period=period,
            region_validation_period=region_validation_period)
        logger.info("\t\tsub-report: {}".format(urenas_agg))

        # URENI
        ureni_exp, ureni_agg, ureni_expv = handle_district_validation(
            district=district,
            report_class=ReportClass.get_or_none("nut_ureni_monthly_routine"),
            report_class_agg=ReportClass.get_or_none(
                "nut_ureni_monthly_routine_aggregated"),
            period=period,
            region_validation_period=region_validation_period)
        logger.info("\t\tsub-report: {}".format(ureni_agg))

        # STOCKS
        stocks_exp, stocks_agg, stocks_expv = handle_district_validation(
            district=district,
            report_class=ReportClass.get_or_none("nut_stocks_monthly_routine"),
            report_class_agg=ReportClass.get_or_none(
                "nut_stocks_monthly_routine_aggregated"),
            period=period,
            region_validation_period=region_validation_period)
        logger.info("\t\tsub-report: {}".format(stocks_agg))

        # AggNutritionR
        nut_exp, nut_agg, nut_expv = handle_district_validation(
            district=district,
            report_class=ReportClass.get_or_none("nutrition_monthly_routine"),
            report_class_agg=ReportClass.get_or_none(
                "nutrition_monthly_routine_aggregated"),
            period=period,
            region_validation_period=region_validation_period)

        nut_agg.urenam_report = urenam_agg
        nut_agg.urenas_report = urenas_agg
        nut_agg.ureni_report = ureni_agg
        nut_agg.stocks_report = stocks_agg
        nut_agg.save()
        logger.info("\t\tmaster-report: {}".format(nut_agg))

        # send notification to Region
        for recipient in Provider.active.filter(
                role=charge_sis, location=nut_agg.entity.get_health_region()):

            Notification.create(
                provider=recipient,
                deliver=Notification.TODAY,
                expirate_on=region_validation_period.end_on,
                category=PROJECT_BRAND,
                text="Le rapport (aggrégé) de routine Nutrition mensuel "
                     "de {period} pour {entity} est prêt. "
                     "No reçu: #{receipt}. "
                     "Vous devez le valider avant le 25."
                     .format(entity=nut_agg.entity.display_full_name(),
                             period=nut_agg.period,
                             receipt=nut_agg.receipt)
                )


def generate_region_country_reports(period,
                                    ensure_correct_date=True):

    logger.info("Switching to {}".format(period))

    if ensure_correct_date:
        now = timezone.now()
        if not period.following().includes(now) \
                or not now.day == ROUTINE_REGION_AGG_DAY:
            logger.error("Not allowed to generate district agg "
                         "outside the 26th of the following period")
            return False

    regions = get_regions()

    # loop on all regions
    for region in regions:

        logger.info("\tAt region {}".format(region))

        # URENAM
        logger.info("\t\tURENAM")
        urenam_exp, urenam_agg = handle_region_validation(
            region=region,
            report_class_agg=ReportClass.get_or_none(
                "nut_urenam_monthly_routine_aggregated"),
            period=period)

        # URENAS
        logger.info("\t\tURENAS")
        urenas_exp, urenas_agg = handle_region_validation(
            region=region,
            report_class_agg=ReportClass.get_or_none(
                "nut_urenas_monthly_routine_aggregated"),
            period=period)

        # URENI
        logger.info("\t\tURENI")
        ureni_exp, ureni_agg = handle_region_validation(
            region=region,
            report_class_agg=ReportClass.get_or_none(
                "nut_ureni_monthly_routine_aggregated"),
            period=period)

        # STOCKS
        logger.info("\t\tSTOCKS")
        stocks_exp, stocks_agg = handle_region_validation(
            region=region,
            report_class_agg=ReportClass.get_or_none(
                "nut_stocks_monthly_routine_aggregated"),
            period=period)

        # AggNutritionR
        logger.info("\t\tMASTER")
        nut_exp, nut_agg = handle_region_validation(
            region=region,
            report_class_agg=ReportClass.get_or_none(
                "nutrition_monthly_routine_aggregated"),
            period=period)
        nut_agg.urenam_report = urenam_agg
        nut_agg.urenas_report = urenas_agg
        nut_agg.ureni_report = ureni_agg
        nut_agg.stocks_report = stocks_agg
        nut_agg.save()

    # COUNTRY LEVEL
    country = mali
    logger.info("\tAt {}".format(country))

    # URENAM
    logger.info("\t\tURENAM")
    urenam_exp, urenam_agg = handle_country_validation(
        country=country,
        report_class_agg=ReportClass.get_or_none(
            "nut_urenam_monthly_routine_aggregated"),
        period=period)

    # URENAS
    logger.info("\t\tURENAS")
    urenas_exp, urenas_agg = handle_country_validation(
        country=country,
        report_class_agg=ReportClass.get_or_none(
            "nut_urenas_monthly_routine_aggregated"),
        period=period)

    # URENI
    logger.info("\t\tURENI")
    ureni_exp, ureni_agg = handle_country_validation(
        country=country,
        report_class_agg=ReportClass.get_or_none(
            "nut_ureni_monthly_routine_aggregated"),
        period=period)

    # STOCKS
    logger.info("\t\tSTOCKS")
    stocks_exp, stocks_agg = handle_country_validation(
        country=country,
        report_class_agg=ReportClass.get_or_none(
            "nut_stocks_monthly_routine_aggregated"),
        period=period)

    # AggNutritionR
    logger.info("\t\tMASTER")
    nut_exp, nut_agg = handle_country_validation(
        country=country,
        report_class_agg=ReportClass.get_or_none(
            "nutrition_monthly_routine_aggregated"),
        period=period)
    nut_agg.urenam_report = urenam_agg
    nut_agg.urenas_report = urenas_agg
    nut_agg.ureni_report = ureni_agg
    nut_agg.stocks_report = stocks_agg
    nut_agg.save()

    # send notification to National level
    for recipient in Provider.active.filter(location__level=0):

        Notification.create(
            provider=recipient,
            deliver=Notification.TODAY,
            expirate_on=nut_agg.period.following().following().start_on,
            category=PROJECT_BRAND,
            text="Le rapport national (aggrégé) de routine Nutrition mensuel "
                 "pour {period} est disponible. No reçu: #{receipt}."
                 .format(period=nut_agg.period, receipt=nut_agg.receipt))
