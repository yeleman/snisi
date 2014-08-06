#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim: ai ts=4 sts=4 et sw=4 nu

from __future__ import (unicode_literals, absolute_import,
                        division, print_function)
import logging

from django.core.management.base import BaseCommand
from optparse import make_option
from py3compat import PY2

from snisi_core.models.Entities import AdministrativeEntity as AEntity

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

        headers = ['name', 'region', 'cercle_commune', 'commune_quartier']
        f = open(options.get('filename'), 'w')
        csv_writer = csv.DictWriter(f, fieldnames=headers)

        csv_writer.writeheader()

        csv_writer.writerow({
            'name': "label",
            'region': "Région",
            'cercle_commune': "Cercle",
            'commune_quartier': "Commune",
        })

        for region in AEntity.objects.filter(type__slug='region'):
            logger.info(region)

            is_bko = region.name == 'BAMAKO'
            for cercle in AEntity.objects.filter(parent=region):
                logger.info(cercle)
                for commune in AEntity.objects.filter(parent=cercle):
                    logger.info(commune)
                    if not is_bko:
                        csv_writer.writerow({
                            'name': "choice_label",
                            'region': region.name,
                            'cercle_commune': cercle.name,
                            'commune_quartier': commune.name
                        })
                        continue
                    for vfq in AEntity.objects.filter(parent=commune):
                        for v in (region, cercle, commune, vfq):
                            if not len(v.name.strip()):
                                continue
                        csv_writer.writerow({
                            'name': "choice_label",
                            'region': region.name,
                            'cercle_commune': commune.name,
                            'commune_quartier': vfq.name
                        })
        f.close()
