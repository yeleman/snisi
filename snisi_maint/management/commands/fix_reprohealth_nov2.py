#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim: ai ts=4 sts=4 et sw=4 nu

from __future__ import (unicode_literals, absolute_import,
                        division, print_function)
import logging

from django.core.management.base import BaseCommand
from django.core.management import call_command

from snisi_core.models.Entities import Entity
from snisi_core.models.Periods import MonthPeriod
from snisi_core.models.Reporting import ExpectedReporting
from snisi_core.models.Projects import Cluster, Participation
from snisi_reprohealth.models.PFActivities import (PFActivitiesR,
                                                   AggPFActivitiesR)
from snisi_reprohealth.aggregations import (generate_district_reports,
                                            generate_region_country_reports)


logger = logging.getLogger(__name__)


class Command(BaseCommand):

    def handle(self, *args, **options):

        cluster = Cluster.get_or_none("msi_reprohealth_routine")

        # delete all reports and cluster participation from segou
        segou = Entity.get_or_none("2732")
        all_segou_entities = [segou] + segou.get_health_districts() \
            + segou.get_health_centers()

        logger.info("Deleting PFActivities AggPFActivitiesR")
        for report in list(PFActivitiesR.objects.all()) + \
                list(AggPFActivitiesR.objects.all()):
            if report.entity.get_health_region() == segou:
                logger.info(report)
                report.delete()

        logger.info("Deleting ExpectedReporting")
        ExpectedReporting.objects.filter(
            entity__in=all_segou_entities,
            report_class__slug__in=["msi_pf_monthly_routine",
                                    "msi_pf_monthly_routine_aggregated"]) \
            .delete()

        logger.info("Deleting Participation")
        for entity in all_segou_entities:
            try:
                Participation.objects.get(
                    cluster=cluster, entity=entity).delete()
            except Participation.DoesNotExist:
                pass

        logger.info("Regenerating cluster caches")
        call_command("update-cluster-caches")

        # regen AggPFActivitiesR
        logger.info("Delete all AggPFActivitiesR")
        AggPFActivitiesR.objects.all().delete()
        period = MonthPeriod.from_url_str("10-2014")
        generate_district_reports(period, ensure_correct_date=False)
        generate_region_country_reports(period, ensure_correct_date=False)

        logger.info("Done")
