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

        headers = ['action', 'slug', 'parent', 'health_entity', 'name',
                   'type', 'main_entity_distance', 'population']
        input_csv_file = open(options.get('filename'), 'r')
        csv_reader = csv.DictReader(input_csv_file, fieldnames=headers)

        for entry in csv_reader:
            if csv_reader.line_num == 1:
                continue
            logger.debug(entry)

            if entry.get('action') == 'create':
                logger.info("Creating {}".format(entry.get('name')))
                slug = entry.get('slug').upper() or None
                parent = Entity.get_or_none(entry.get('parent'))
                etype = EntityType.get_or_none(entry.get('type'))
                hcls = AdministrativeEntity

                if slug is None:
                    slug = "{}{}".format(
                        parent.slug[:-3],
                        str(sorted([int(v.slug[-3:])
                                    for v in parent.get_vfqs()
                                    if v.slug.startswith(
                                        parent.slug[:-3])])[-1] + 1)
                        .zfill(3))

                entity = hcls.objects.create(
                    slug=slug,
                    name=entry.get('name').upper(),
                    type=etype,
                    parent=parent)
                if entry.get('health_entity'):
                    health_entity = Entity.get_or_none(
                        entry.get('health_entity'))
                    entity.health_entity = health_entity
                    entity.save()
                if entry.get('main_entity_distance'):
                    entity.main_entity_distance = int(
                        entry.get('main_entity_distance'))
                entity.save()
            elif entry.get('action') == 'disable':
                entity = Entity.get_or_none(entry.get('slug'))
                logger.info("Disabling {}".format(entity))
                entity.active = False
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
                if entry.get('health_entity'):
                    health_entity = Entity.get_or_none(
                        entry.get('health_entity'))
                    entity.health_entity = health_entity
                    entity.save()
                if entry.get('main_entity_distance'):
                    entity.main_entity_distance = int(
                        entry.get('main_entity_distance'))
                    entity.save()

        logger.info("Done")
