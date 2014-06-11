#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim: ai ts=4 sts=4 et sw=4 nu

from __future__ import (unicode_literals, absolute_import,
                        division, print_function)
import logging
import os
import datetime

from django.utils import timezone
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
        make_option('-c',
                    help='Cluster slug',
                    action='store',
                    dest='cluster_slug'),
        make_option('-f',
                    help='CSV file',
                    action='store',
                    dest='filename'),
        make_option('-s',
                    help='Start Date (YYYY-mm-dd)',
                    action='store',
                    dest='start_date'),
        make_option('-n',
                    help='Mark as not active',
                    action='store_true',
                    default=False,
                    dest='not_active'),
    )

    def handle(self, *args, **options):

        cluster = Cluster.get_or_none(options.get('cluster_slug'))
        if cluster is None:
            logger.error("Cluster `{}` does not exist.".format(options.get('cluster_slug')))
            return

        if not os.path.exists(options.get('filename') or ""):
            logger.error("CSV file `{}` does not exist.".format(options.get('filename')))
            return

        headers = ['SNISI', 'Name']
        input_csv_file = open(options.get('filename'), 'r')
        csv_reader = csv.DictReader(input_csv_file, fieldnames=headers)

        try:
            modified_on = datetime.datetime(*[int(e) for e in options.get('start_date', '').split('-')])
        except:
            modified_on = timezone.now()

        for entry in csv_reader:
            if csv_reader.line_num == 1:
                continue

            entity = Entity.get_or_none(entry.get('SNISI'))
            if entity is None:
                logger.warning("Entity `{}` does not exist.".format(entry.get('SNISI')))
                continue

            p, created = Participation.objects.get_or_create(
                cluster=cluster,
                entity=entity,
                is_active=not options.get('not_active'),
                modified_on=modified_on)
            logger.info(p)
