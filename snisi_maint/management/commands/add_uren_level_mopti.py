#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim: ai ts=4 sts=4 et sw=4 nu

from __future__ import (unicode_literals, absolute_import,
                        division, print_function)
import logging

from django.utils import timezone
from django.core.management.base import BaseCommand

from snisi_core.models.Entities import Entity
from snisi_core.models.Projects import Cluster, Participation


logger = logging.getLogger(__name__)


class Command(BaseCommand):

    def handle(self, *args, **options):

        cluster = Cluster.get_or_none("nutrition_routine")
        cluster_sms = Cluster.get_or_none("nutrition_routine_sms")

        mopti = Entity.get_or_none("SSH3")
        mali = Entity.get_or_none("mali")

        csrefs = [
            'NM34',  # BANDIAGARA
            'JHD6',  # BANKASS
            'HP42',  # DJENNE
            'KGW3',  # DOUENTZA
            '2AY4',  # KORO
            'J5C6',  # MOPTI
            'ERR5',  # TENENKOU
            '6770',  # YOUWAROU
        ]

        for entity in mopti.get_health_centers() + \
                mopti.get_health_districts() + [mopti, mali]:

            logger.info(entity)

            if entity.type.slug == 'health_center':
                entity.has_urenam = True
                entity.has_urenas = True
                entity.has_ureni = False

                if entity.slug in csrefs:
                    entity.has_ureni = True

                    # set the CSRéf as main entity on CSCom's.
                    for e in entity.get_health_district().get_health_centers():
                        e.main_entity = entity
                        e.save()

                entity.save()

            p, created = Participation.objects.get_or_create(
                cluster=cluster,
                entity=entity,
                is_active=True,
                modified_on=timezone.now())
            logger.info(p)

            if entity.type.slug == 'health_center':
                p, created = Participation.objects.get_or_create(
                    cluster=cluster_sms,
                    entity=entity,
                    is_active=True,
                    modified_on=timezone.now())
                logger.info(p)
