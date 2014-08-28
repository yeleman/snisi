#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim: ai ts=4 sts=4 et sw=4 nu

from __future__ import (unicode_literals, absolute_import,
                        division, print_function)
import datetime
import logging

from py3compat import PY2
from optparse import make_option
from django.core.management.base import BaseCommand
from django.utils import timezone

from snisi_core.models.Entities import Entity
from snisi_core.models.Periods import MonthPeriod
from snisi_core.models.Projects import Cluster, Participation
from snisi_tools.datetime import DEBUG_change_system_date

if PY2:
    import unicodecsv as csv
else:
    import csv

logger = logging.getLogger(__name__)


class Command(BaseCommand):

    option_list = BaseCommand.option_list + (
        make_option('-f',
                    help='CSV file to import Health Entities from',
                    action='store',
                    dest='input_file'),
        make_option('-c',
                    help='Delete all Participations to clusters first',
                    action='store_true',
                    dest='clear')
        )

    def handle(self, *args, **options):

        msi_cluster = Cluster.objects.get(slug="msi_reprohealth_routine")
        msi_cluster_sms = \
            Cluster.objects.get(slug="msi_reprohealth_routine_sms")
        DEBUG_change_system_date(
            MonthPeriod.from_url_str("08-2012").end_on
            - datetime.timedelta(days=5), True)

        headers = ['SNISI', 'Name', 'Type']
        input_file = open(options.get('input_file'), 'r')
        csv_reader = csv.DictReader(input_file, fieldnames=headers)

        if options.get('clear'):
            Participation.objects.filter(
                cluster__in=[msi_cluster, msi_cluster_sms]).delete()

        for entry in csv_reader:
            if csv_reader.line_num == 1:
                continue

            health_unit = Entity.get_or_none(entry.get('SNISI'))
            if health_unit is None:
                continue

            logger.info(health_unit)

            p, created = Participation.objects.get_or_create(
                cluster=msi_cluster,
                entity=health_unit,
                modified_on=timezone.now())
            p, created = Participation.objects.get_or_create(
                cluster=msi_cluster_sms,
                entity=health_unit,
                modified_on=timezone.now())

        DEBUG_change_system_date(None, True)
