#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim: ai ts=4 sts=4 et sw=4 nu

from __future__ import (unicode_literals, absolute_import,
                        division, print_function)
import logging

from django.core.management.base import BaseCommand

from snisi_core.models.Entities import Entity
from snisi_core.models.Projects import Cluster, Participation

logger = logging.getLogger(__name__)


class Command(BaseCommand):

    def handle(self, *args, **options):

        mali = Entity.get_or_none("mali")
        drmopti = Entity.get_or_none("SSH3")
        dsmopti = Entity.get_or_none("HFD9")
        dsbandiagara = Entity.get_or_none("MJ86")

        cluster = Cluster.get_or_none("malaria_weekly_routine")

        for entity in [mali, drmopti, dsmopti, dsbandiagara] + \
                dsmopti.get_health_centers() + \
                dsbandiagara.get_health_centers():

            p, created = Participation.objects.get_or_create(
                cluster=cluster,
                entity=entity)
            logger.info(p)
