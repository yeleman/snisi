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
from snisi_malaria.models import (AggMalariaR, MalariaR,
                                  AggDailyMalariaR, AggWeeklyMalariaR)
from snisi_malaria import (ROUTINE_DISTRICT_AGG_DAY,
                           ROUTINE_REGION_AGG_DAY)
from snisi_malaria.integrity import PROJECT_BRAND
from snisi_core.models.Notifications import Notification
from snisi_core.models.FixedWeekPeriods import FixedMonthWeek

logger = logging.getLogger(__name__)

autobot = Provider.get_or_none('autobot')
reportcls_slug = "malaria_monthly_routine_aggregated"
daily_reportcls_slug = "malaria_weekly_routine_aggregated"
rclass = ReportClass.get_or_none(reportcls_slug)
daily_rclass = ReportClass.get_or_none(daily_reportcls_slug)
weekly_rclasses = [
    ReportClass.get_or_none('malaria_weekly_routine_firstweek_aggregated'),
    ReportClass.get_or_none('malaria_weekly_routine_secondweek_aggregated'),
    ReportClass.get_or_none('malaria_weekly_routine_thirdweek_aggregated'),
    ReportClass.get_or_none('malaria_weekly_routine_fourthweek_aggregated'),
    ReportClass.get_or_none('malaria_weekly_routine_fifthweek_aggregated'),
]
weekly_wlong_rclasses = [
    ReportClass.get_or_none(
        'malaria_weekly_routine_firstweek_weeklong_aggregated'),
    ReportClass.get_or_none(
        'malaria_weekly_routine_secondweek_weeklong_aggregated'),
    ReportClass.get_or_none(
        'malaria_weekly_routine_thirdweek_weeklong_aggregated'),
    ReportClass.get_or_none(
        'malaria_weekly_routine_fourthweek_weeklong_aggregated'),
    ReportClass.get_or_none(
        'malaria_weekly_routine_fifthweek_weeklong_aggregated'),
]
charge_sis = Role.get_or_none("charge_sis")

mali = Entity.get_or_none("mali")
cluster = Cluster.get_or_none("malaria_monthly_routine")

get_districts = lambda: [e for e in cluster.members()
                         if e.type.slug == 'health_district']
get_regions = lambda: [e for e in cluster.members()
                       if e.type.slug == 'health_region']


def generate_weekly_reports(period, wperiod,
                            ensure_correct_date=False,
                            now=timezone.now):

    if hasattr(now, '__call__'):
        now = now()

    # period = 06-2015
    # fourth_week

    current_week = FixedMonthWeek.current(at=now)
    # wperiod = FixedMonthWeek.previous_week(current_week)

    logger.info("current: {} - wperiod: {}".format(current_week, wperiod))
    logger.info("Switching to {}/{}".format(wperiod, period))

    if ensure_correct_date:
        if not current_week.includes(now):
            raise ValueError("Not allowed to generate weekly agg "
                             "outside of the following period")
        elif now < wperiod.end_on + datetime.timedelta(days=5):
            raise ValueError("Extended Reporting Period not over yet")

    # gen all-levels AggDailyMalariaR for each day
    logger.info("all-levels AggDailyMalariaR for each day")
    for day_period in wperiod.get_day_periods():
        logger.debug("Generating for {}".format(day_period))
        districts = get_districts()
        for district in districts:
            logger.info("\tAt district {}".format(district))

            # ack expected
            exp = ExpectedReporting.objects.filter(
                report_class=daily_rclass,
                entity__slug=district.slug,
                period=day_period)
            # not expected
            if exp.count() == 0:
                continue
            else:
                # might explode if 2 exp but that's the point
                exp = exp.get()

            # create AggMalariaR
            agg = AggDailyMalariaR.create_from(
                period=day_period,
                entity=district,
                created_by=autobot)
            exp.acknowledge_report(agg)

            # validate (no expected validation)
            agg.record_validation(
                validated=True,
                validated_by=autobot,
                validated_on=timezone.now(),
                auto_validated=True)

        regions = get_regions()
        for region in regions:
            logger.info("\tAt region {}".format(region))
            # ack expected
            exp = ExpectedReporting.objects.filter(
                report_class=daily_rclass,
                entity__slug=region.slug,
                period=day_period)
            if exp.count() == 0:
                continue
            else:
                exp = exp.get()

            # create AggDailyMalariaR/region
            agg = AggDailyMalariaR.create_from(
                period=day_period,
                entity=region,
                created_by=autobot)
            exp.acknowledge_report(agg)

            # validate (no expected validation)
            agg.record_validation(
                validated=True,
                validated_by=autobot,
                validated_on=timezone.now(),
                auto_validated=True)

        logger.info("\tAt {}".format(mali))

        # ack expected
        exp = ExpectedReporting.objects.get(
            report_class=daily_rclass,
            entity__slug=mali.slug,
            period=day_period)

        # create AggDailyMalariaR/country
        agg = AggDailyMalariaR.create_from(
            period=day_period,
            entity=mali,
            created_by=autobot)
        exp.acknowledge_report(agg)

        # validate (no expected validation)
        agg.record_validation(
            validated=True,
            validated_by=autobot,
            validated_on=timezone.now(),
            auto_validated=True)

    # gen all-level AggWeeklyMalariaR for period
    logger.info("all-level AggWeeklyMalariaR for period")
    districts = get_districts()
    for district in districts:
        logger.info("\tAt district {}".format(district))

        for hc in district.get_health_centers():
            logger.info("\tAt HC {}".format(hc))

            # ack expected
            exp = ExpectedReporting.objects.filter(
                report_class__in=weekly_wlong_rclasses,
                entity__slug=hc.slug,
                period=wperiod)
            # not expected
            if exp.count() == 0:
                continue
            else:
                # might explode if 2 exp but that's the point
                exp = exp.get()

            # create AggWeeklyMalariaR
            print(exp, exp.satisfied, exp.updated_on)
            agg = AggWeeklyMalariaR.create_from(
                period=wperiod,
                entity=hc,
                created_by=autobot)
            exp.acknowledge_report(agg)

            # validate (no expected validation)
            agg.record_validation(
                validated=True,
                validated_by=autobot,
                validated_on=timezone.now(),
                auto_validated=True)

        # ack expected
        exp = ExpectedReporting.objects.filter(
            report_class__in=weekly_wlong_rclasses,
            entity__slug=district.slug,
            period=wperiod)
        # not expected
        if exp.count() == 0:
            continue
        else:
            # might explode if 2 exp but that's the point
            exp = exp.get()

        # create AggWeeklyMalariaR
        agg = AggWeeklyMalariaR.create_from(
            period=wperiod,
            entity=district,
            created_by=autobot)
        exp.acknowledge_report(agg)

        # validate (no expected validation)
        agg.record_validation(
            validated=True,
            validated_by=autobot,
            validated_on=timezone.now(),
            auto_validated=True)

    regions = get_regions()
    for region in regions:
        logger.info("\tAt region {}".format(region))
        # ack expected
        exp = ExpectedReporting.objects.filter(
            report_class__in=weekly_wlong_rclasses,
            entity__slug=region.slug,
            period=wperiod)
        if exp.count() == 0:
            continue
        else:
            exp = exp.get()

        # create AggWeeklyMalariaR/region
        agg = AggWeeklyMalariaR.create_from(
            period=wperiod,
            entity=region,
            created_by=autobot)
        exp.acknowledge_report(agg)

        # validate (no expected validation)
        agg.record_validation(
            validated=True,
            validated_by=autobot,
            validated_on=timezone.now(),
            auto_validated=True)

    logger.info("\tAt {}".format(mali))

    # ack expected
    exp = ExpectedReporting.objects.get(
        report_class__in=weekly_wlong_rclasses,
        entity__slug=mali.slug,
        period=wperiod)
    if exp is None:
        return

    # create AggWeeklyMalariaR/country
    agg = AggWeeklyMalariaR.create_from(
        period=wperiod,
        entity=mali,
        created_by=autobot)
    exp.acknowledge_report(agg)

    # validate (no expected validation)
    agg.record_validation(
        validated=True,
        validated_by=autobot,
        validated_on=timezone.now(),
        auto_validated=True)


def generate_district_reports(period,
                              ensure_correct_date=True):

    logger.info("Switching to {}".format(period))

    region_validation_period = DefaultRegionValidationPeriod \
        .find_create_by_date(period.following().middle())

    if ensure_correct_date:
        now = timezone.now()
        if not period.following().includes(now) \
                or not now.day == ROUTINE_DISTRICT_AGG_DAY:
            raise ValueError("Not allowed to generate district agg "
                             "outside the 16th of the following period")

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

        exp.acknowledge_report(agg)

        # create expected validation
        ExpectedValidation.objects.create(
            report=agg,
            validation_period=region_validation_period,
            validating_entity=district.get_health_region(),
            validating_role=charge_sis)

        # send notification to Region
        for recipient in Provider.active.filter(
                role=charge_sis, location=agg.entity.get_health_region()):

            Notification.create(
                provider=recipient,
                deliver=Notification.TODAY,
                expirate_on=region_validation_period.end_on,
                category=PROJECT_BRAND,
                text="Le rapport (aggrégé) de routine Paludisme mensuel "
                     "de {period} pour {entity} est prêt. "
                     "No reçu: #{receipt}. "
                     "Vous devez le valider avant le 25."
                     .format(entity=agg.entity.display_full_name(),
                             period=agg.period,
                             receipt=agg.receipt)
                )


def generate_region_country_reports(period,
                                    ensure_correct_date=True):

    logger.info("Switching to {}".format(period))

    if ensure_correct_date:
        now = timezone.now()
        if not period.following().includes(now) \
                or not now.day == ROUTINE_REGION_AGG_DAY:
            raise ValueError("Not allowed to generate district agg "
                             "outside the 16th of the following period")
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

            # ack validation (auto)
            try:
                report = AggMalariaR.objects.get(period=period,
                                                 entity=district)
            except AggMalariaR.DoesNotExist:
                logger.warning("AggMalariaR report missing for DS {}"
                               .format(district))
                continue
            if not report.validated:
                try:
                    expv = ExpectedValidation.objects.get(report=report)
                    expv.acknowledge_validation(
                        validated=True,
                        validated_by=autobot,
                        validated_on=timezone.now(),
                        auto_validated=True)
                except ExpectedValidation.DoesNotExist:
                    pass

        # create AggMalariaR/region
        agg = AggMalariaR.create_from(
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

    logger.info("\tAt {}".format(mali))

    # ack expected
    exp = ExpectedReporting.objects.get(
        report_class=rclass,
        entity__slug=mali.slug,
        period=period)

    if exp is None:
        return

    # create AggMalariaR/country
    agg = AggMalariaR.create_from(
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

    # send notification to National level
    for recipient in Provider.active.filter(location__level=0):

        Notification.create(
            provider=recipient,
            deliver=Notification.TODAY,
            expirate_on=agg.period.following().following().start_on,
            category=PROJECT_BRAND,
            text="Le rapport national (aggrégé) de routine Paludisme mensuel "
                 "pour {period} est disponible. No reçu: #{receipt}."
                 .format(period=agg.period, receipt=agg.receipt)
            )
