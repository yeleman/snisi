#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim: ai ts=4 sts=4 et sw=4 nu

from __future__ import (unicode_literals, absolute_import,
                        division, print_function)
import logging

from django.core.management.base import BaseCommand
from optparse import make_option
from py3compat import PY2

from snisi_core.models.Providers import Provider
from snisi_core.models.Entities import Entity

if PY2:
    import unicodecsv as csv
else:
    import csv

logger = logging.getLogger(__name__)


class Command(BaseCommand):

    option_list = BaseCommand.option_list + (
        make_option('-r',
                    help='Region Code',
                    action='store',
                    dest='region_slug'),
    )

    def handle(self, *args, **options):

        region = Entity.get_or_none(options.get('region_slug'))
        if region is None:
            logger.error("Incorrect Region slug `{}`"
                         .format(options.get('region_slug')))
            return

        created = [u.strip() for u in open('created.txt', 'r').readlines()]

        headers = ['Nom', 'Prénom', 'Role', 'Localité',
                   'SNISI', 'Numéro Flotte',
                   'Identifiant', 'Mot de passe',
                   'Emargement']

        for district in region.get_health_districts():
            logger.info(district.display_code_name())

            health_centers = district.get_health_centers()
            providers = Provider.objects.filter(
                location__in=health_centers + [district]).order_by('last_name')
            # providers.sort(key=lambda x: x.get_full_name())

            output_csv_file = open(
                'district-{}.csv'.format(district.name), 'w')
            csv_writer = csv.DictWriter(output_csv_file, fieldnames=headers)

            csv_writer.writeheader()

            for provider in providers:
                passwd = "aaaa" if provider.username in created else ""
                csv_writer.writerow({
                    'Nom': provider.last_name,
                    'Prénom': provider.first_name,
                    'Role': provider.role,
                    'Localité': provider.location.name,
                    'Code SNISI': provider.location.slug,
                    'Identifiant': provider.username,
                    'Mot de passe': passwd,
                    })

            output_csv_file.close()
