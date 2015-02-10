#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim: ai ts=4 sts=4 et sw=4 nu

from __future__ import (unicode_literals, absolute_import,
                        division, print_function)
import logging
import os

from django.core.management.base import BaseCommand
from optparse import make_option
from py3compat import PY2

from snisi_core.models.Entities import Entity
from snisi_core.models.Projects import Cluster, Participation

if PY2:
    import unicodecsv as csv
else:
    import csv

logger = logging.getLogger(__name__)


class Command(BaseCommand):

    option_list = BaseCommand.option_list + (
        make_option('-f',
                    help='CSV file',
                    action='store',
                    dest='filename'),
    )

    def handle(self, *args, **options):

        if not os.path.exists(options.get('filename') or ""):
            logger.error("CSV file `{}` does not exist."
                         .format(options.get('filename')))
            return

        headers = ['action', 'slug', 'cluster', 'include_hc']
        input_csv_file = open(options.get('filename'), 'r')
        csv_reader = csv.DictReader(input_csv_file, fieldnames=headers)

        for entry in csv_reader:
            if csv_reader.line_num == 1:
                continue

            entity = Entity.get_or_none(entry.get('slug'))
            if entity is None:
                logger.warning("Entity `{}` does not exist."
                               .format(entry.get('SNISI')))
                continue

            cluster = Cluster.get_or_none(entry.get('cluster'))
            if cluster is None:
                logger.error("Cluster `{}` does not exist."
                             .format(options.get('cluster_slug')))
                continue

            include_hc = bool(entry.get('include_hc'))
            entities = [entity]
            if include_hc:
                entities += entity.get_health_centers()

            if entry.get('action') == 'add':
                for e in entities:
                    p, created = Participation.objects.get_or_create(
                        cluster=cluster,
                        entity=e,
                        is_active=True)
                    logger.info(p)

            if entry.get('action') == 'disable':
                for p in Participation.objects.filter(
                        cluster=cluster,
                        entity__slug__in=[e.slug for e in entities]):
                    p.is_active = False
                    p.save()
                    logger.info(p)

            if entry.get('action') == 'enable':
                for p in Participation.objects.filter(
                        cluster=cluster,
                        entity__slug__in=[e.slug for e in entities]):
                    p.is_active = True
                    p.save()
                    logger.info(p)

            if entry.get('action') == 'remove':
                Participation.objects.filter(
                    cluster=cluster,
                    entity__slug__in=[e.slug for e in entities]).delete()

        logger.info("All Done")
