#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim: ai ts=4 sts=4 et sw=4 nu

from __future__ import (unicode_literals, absolute_import,
                        division, print_function)

from py3compat import PY2
from optparse import make_option
from django.core.management.base import BaseCommand
from django.core.management import call_command

if PY2:
    import unicodecsv as csv
else:
    import csv

from snisi_core.models.Entities import (Entity, AdministrativeEntity,
                                        HealthEntity, EntityType)


class Command(BaseCommand):

    option_list = BaseCommand.option_list + (
        make_option('-a',
                    help='CSV file to import Administrative Entities from',
                    action='store',
                    dest='input_admin_file'),
        make_option('-f',
                    help='CSV file to import Health Entities from',
                    action='store',
                    dest='input_health_file'),
        make_option('-c',
                    help='Delete all Entity fixtures first',
                    action='store_true',
                    dest='clear')
        )

    def handle(self, *args, **options):

        admin_headers = ['IDENT_Code', 'IDENT_Name',
                         'IDENT_Type', 'IDENT_ParentCode',
                         'IDENT_ModifiedOn', 'IDENT_RegionName',
                         'IDENT_CercleName',
                         'IDENT_CommuneName',
                         'IDENT_HealthAreaCode', 'IDENT_HealthAreaName',
                         'IDENT_HealthAreaCenterDistance',
                         'IDENT_Latitude', 'IDENT_Longitude', 'IDENT_Geometry']

        health_headers = ['IDENT_Code', 'IDENT_Name', 'IDENT_Type',
                          'IDENT_ParentCode',
                          'IDENT_ModifiedOn',
                          'IDENT_HealthRegionCode', 'IDENT_HealthDistrictCode',
                          'IDENT_HealthAreaCode', 'IDENT_MainEntityCode',
                          'IDENT_Latitude', 'IDENT_Longitude',
                          'IDENT_Geometry']

        input_admin_file = open(options.get('input_admin_file'), 'r')
        admin_csv_reader = csv.DictReader(input_admin_file,
                                          fieldnames=admin_headers)

        input_health_file = open(options.get('input_health_file'), 'r')
        health_csv_reader = csv.DictReader(input_health_file,
                                           fieldnames=health_headers)

        if options.get('clear'):
            print("Removing all entities...")
            AdministrativeEntity.objects.all().delete()
            HealthEntity.objects.all().delete()
            Entity.objects.all().delete()
            print("Importing fixtures")
            call_command("loaddata", "snisi_core/fixtures/EntityType.xml")
            call_command("loaddata", "snisi_core/fixtures/Entity-root.xml")

        def add_entity(entity_dict, is_admin):
            cls = AdministrativeEntity if is_admin else HealthEntity
            slug = entry.get('IDENT_Code')
            name = entry.get('IDENT_Name')
            type_slug = entry.get('IDENT_Type')
            entity_type = EntityType.objects.get(slug=type_slug)
            parent_slug = entry.get('IDENT_ParentCode')
            latitude = entry.get('IDENT_Latitude')
            longitude = entry.get('IDENT_Longitude')
            geometry = entry.get('IDENT_Geometry')
            health_area_slug = entry.get('IDENT_HealthAreaCode')
            try:
                health_area_center_distance = float(
                    entry.get('IDENT_HealthAreaCenterDistance'))
            except:
                health_area_center_distance = None
            if health_area_slug:
                health_area = Entity.get_or_none(health_area_slug)
            else:
                health_area = None

            entity = cls.objects.create(slug=slug,
                                        name=name,
                                        type=entity_type,
                                        latitude=latitude or None,
                                        longitude=longitude or None,
                                        geometry=geometry or None)
            if parent_slug:
                parentcls = Entity if parent_slug == 'mali' else cls
                parent = parentcls.objects.get(slug=parent_slug)
                entity.parent = parent

            if cls == AdministrativeEntity and health_area:
                entity.health_entity = health_area
                entity.main_entity_distance = health_area_center_distance

            entity.save()

            print(entity.name)

        print("Importing Health Entities...")
        for entry in health_csv_reader:
            if health_csv_reader.line_num == 1:
                continue

            add_entity(entry, False)

        print("Importing Admin Entities...")
        for entry in admin_csv_reader:
            if admin_csv_reader.line_num == 1:
                continue

            add_entity(entry, True)

        print("Updating Health Entities with main center")
        input_health_file.seek(0)
        health_csv_reader = csv.DictReader(input_health_file,
                                           fieldnames=health_headers)
        for entry in health_csv_reader:
            if health_csv_reader.line_num == 1:
                continue

            if not entry.get('IDENT_MainEntityCode'):
                continue

            entity = HealthEntity.objects.get(slug=entry.get('IDENT_Code'))
            entity.main_entity = HealthEntity.objects.get(
                slug=entry.get('IDENT_MainEntityCode'))
            entity.save()
