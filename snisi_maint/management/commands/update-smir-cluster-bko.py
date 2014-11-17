#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim: ai ts=4 sts=4 et sw=4 nu

from __future__ import (unicode_literals, absolute_import,
                        division, print_function)
import logging

from django.core.management.base import BaseCommand

from snisi_core.models.Entities import Entity
from snisi_core.models.Providers import Provider
from snisi_core.models.Groups import Group
from snisi_core.models.Projects import Cluster, Participation


logger = logging.getLogger(__name__)

response_team = [
    'rgaudin',
]


class Command(BaseCommand):

    def handle(self, *args, **options):

        mali = Entity.get_or_none("mali")
        segou = Entity.get_or_none("2732")
        mopti = Entity.get_or_none("SSH3")
        bamako = Entity.get_or_none("9GR8")

        entities = [mali] + \
            [e for region in (segou, mopti, bamako)
             for e in region.get_health_centers() +
             region.get_health_districts()]

        cluster = Cluster.get_or_none("epidemiology_routine")

        for entity in entities:

            if entity is None:
                continue

            p, created = Participation.objects.get_or_create(
                cluster=cluster,
                entity=entity,
                is_active=True)
            if created:
                logger.info(p)

        # create group
        group = Group.get_or_none("smir_alert_response")
        if group is None:
            group = Group(slug="smir_alert_response",
                          name="Réponse Alertes SMIR")
            group.save()
            for username in response_team:
                group.members.add(Provider.get_or_none(username))
