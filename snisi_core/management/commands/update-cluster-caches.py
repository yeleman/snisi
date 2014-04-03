#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim: ai ts=4 sts=4 et sw=4 nu

from __future__ import (unicode_literals, absolute_import,
                        division, print_function)
import logging

from django.core.management.base import BaseCommand
from snisi_core.models.Projects import Cluster

logger = logging.getLogger(__name__)


class Command(BaseCommand):

    def handle(self, *args, **options):

        for cluster in Cluster.active.all():
            logger.info("Cluster {}".format(cluster))

            update_cluster_caches_for = cluster.domain.import_from('caching.update_cluster_caches_for')
            if update_cluster_caches_for is None:
                logger.info("\t Skipping cluster {}".format(cluster))
                continue

            update_cluster_caches_for(cluster)
            logger.info("Done updating cache for {}".format(cluster))
