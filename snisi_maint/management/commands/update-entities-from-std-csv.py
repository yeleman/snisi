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

from snisi_core.models.Entities import (
    Entity, HealthEntity, AdministrativeEntity, EntityType)

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

        headers = ['action', 'slug', 'parent', 'name', 'type',
                   'has_urenam', 'has_urenas', 'has_ureni', 'main_entity']
        input_csv_file = open(options.get('filename'), 'r')
        csv_reader = csv.DictReader(input_csv_file, fieldnames=headers)

        has_matrix = {
            'y': True,
            'n': False
        }

        for entry in csv_reader:
            if csv_reader.line_num == 1:
                continue
            logger.debug(entry)

            if entry.get('action') == 'create':
                logger.info("Creating {}".format(entry.get('name')))
                parent = Entity.get_or_none(entry.get('parent'))
                etype = EntityType.get_or_none(entry.get('type'))
                hcls = HealthEntity if etype.slug.startswith('health_') \
                    else AdministrativeEntity
                entity = hcls.objects.create(
                    slug=entry.get('slug').upper(),
                    name=entry.get('name').upper(),
                    type=etype,
                    parent=parent)
                if entry.get('has_urenam') == 'y':
                    entity.has_urenam = True
                if entry.get('has_urenas') == 'y':
                    entity.has_urenas = True
                if entry.get('has_ureni') == 'y':
                    entity.has_ureni = True
                entity.save()
            elif entry.get('action') == 'disable':
                entity = Entity.get_or_none(entry.get('slug'))
                logger.info("Disabling {}".format(entity))
                entity.active = False
                entity.save()
            elif entry.get('action') == 'enable':
                entity = Entity.get_or_none(entry.get('slug'))
                logger.info("Enabling {}".format(entity))
                entity.active = True
                entity.save()
            elif entry.get('action') == 'update':
                entity = Entity.get_or_none(entry.get('slug'))
                logger.info("Updating {}".format(entity))
                if entry.get('name'):
                    entity.name = entry.get('name').upper()
                    entity.save()
                if entry.get('type'):
                    etype = EntityType.get_or_none(entry.get('type'))
                    entity.type = etype
                    entity.save()
                if entry.get('parent'):
                    parent = Entity.get_or_none(entry.get('parent'))
                    entity.parent = parent
                    entity.save()
                # update main_entity ?
                if entry.get('main_entity'):
                    main_entity = Entity.get_or_none(entry.get('main_entity'))
                    entity.main_entity = main_entity
                    entity.save()
                if entry.get('has_urenam'):
                    entity.has_urenam = has_matrix.get(
                        entry.get('has_urenam').lower(), False)
                    entity.save()
                if entry.get('has_urenas'):
                    entity.has_urenas = has_matrix.get(
                        entry.get('has_urenas').lower(), False)
                    entity.save()
                if entry.get('has_ureni'):
                    entity.has_ureni = has_matrix.get(
                        entry.get('has_ureni').lower(), False)
                    entity.save()

        logger.info("Done")
