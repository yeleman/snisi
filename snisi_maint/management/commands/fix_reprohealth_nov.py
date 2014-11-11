#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim: ai ts=4 sts=4 et sw=4 nu

from __future__ import (unicode_literals, absolute_import,
                        division, print_function)
import logging

from django.core.management.base import BaseCommand

from snisi_core.models.Periods import MonthPeriod
from snisi_core.models.Entities import Entity
from snisi_core.models.Reporting import ExpectedReporting
from snisi_core.models.Projects import Cluster, Participation
from snisi_core.models.PeriodicTasks import PeriodicTask
from snisi_reprohealth.models.PFActivities import (PFActivitiesR,
                                                   AggPFActivitiesR)


logger = logging.getLogger(__name__)


class Command(BaseCommand):

    def handle(self, *args, **options):

        # delete all reports from koulikoro
        kkr = Entity.get_or_none("4JN7")

        for report in list(PFActivitiesR.objects.all()) + \
                list(AggPFActivitiesR.objects.all()):
            if report.entity.get_health_region() == kkr:
                logger.info(report)
                report.delete()

        # delete all reports from August
        before_october = [MonthPeriod.from_url_str("08-2014"),
                          MonthPeriod.from_url_str("09-2014")]
        PFActivitiesR.objects.filter(period__in=before_october).delete()

        # delete all Expected from August
        ExpectedReporting.objects.filter(
            period__in=before_october,
            report_class__slug__in=["msi_pf_monthly_routine",
                                    "msi_pf_monthly_routine_aggregated"]) \
            .delete()

        # delete all aggregated
        AggPFActivitiesR.objects.all().delete()

        # delete september and october tasks
        for slug in ['reprohealth_10-2014_end_of_region_period',
                     'reprohealth_10-2014_end_of_district_period',
                     'reprohealth_09-2014_end_of_region_period',
                     'reprohealth_09-2014_end_of_district_period']:
            try:
                p = PeriodicTask.objects.get(slug=slug)
            except:
                continue
            logger.info(p)
            p.delete()

        # add missing entities to cluster
        districts = [Entity.get_or_none(s) for s in
                     [u'W6D2', u'RN42', u'YF98', u'8GK0', u'HFD9',
                      u'ZWT5', u'D2K8', u'N696', u'8R92', u'MJ86', u'5B40']]

        mali = Entity.get_or_none("mali")
        segou = Entity.get_or_none("2732")
        mopti = Entity.get_or_none("SSH3")
        bko = Entity.get_or_none("9GR8")
        entities = [mali] + districts + [mopti, segou, kkr]
        cluster = Cluster.get_or_none("msi_reprohealth_routine")
        for entity in entities:
            if entity is None:
                continue

            p, created = Participation.objects.get_or_create(
                cluster=cluster,
                entity=entity,
                is_active=True)
            if created:
                logger.info(p)

        # remove bamako region from cluster
        try:
            Participation.objects.get(cluster=cluster, entity=bko).delete()
        except Participation.DoesNotExist:
            pass
