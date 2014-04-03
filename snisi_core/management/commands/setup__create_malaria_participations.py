#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim: ai ts=4 sts=4 et sw=4 nu

from __future__ import (unicode_literals, absolute_import,
                        division, print_function)
import json
import datetime

from optparse import make_option
from django.core.management.base import BaseCommand
from django.utils.timezone import utc

from snisi_core.models.Entities import HealthEntity, Entity
from snisi_core.models.Projects import Participation, Cluster


class Command(BaseCommand):

    option_list = BaseCommand.option_list + (
        make_option('-f',
                    help='JSON matrix of old and new codes',
                    action='store',
                    dest='input_file'),
        make_option('-c',
                    help='Delete all malara Participations first',
                    action='store_true',
                    dest='clear')
        )

    def handle(self, *args, **options):

        input_file = open(options.get('input_file'), 'r')
        matrix = json.load(input_file)

        # malaria_proj = get_domain()
        routine_cluster = Cluster.get_or_none("malaria_monthly_routine")
        routine_cluster_sms = Cluster.get_or_none("malaria_monthly_routine_sms")
        mopti = Entity.get_or_none("SSH3")
        moptid = Entity.get_or_none("HFD9")
        segou_start = datetime.datetime(2011, 6, 20).replace(tzinfo=utc)
        moptid_start = datetime.datetime(2013, 8, 20).replace(tzinfo=utc)
        moptio_start = datetime.datetime(2013, 12, 20).replace(tzinfo=utc)

        if options.get('clear'):
            print("Removing all malaria participations...")
            Participation.objects.filter(cluster=routine_cluster).delete()
            Participation.objects.filter(cluster=routine_cluster_sms).delete()

        print("Creating Participation...")

        for new, old in matrix['new_old'].items():
            cls = Entity if new == 'mali' else HealthEntity
            entity = cls.objects.get(slug=new)

            if entity in mopti.get_health_descendants():
                if entity in moptid.get_health_descendants():
                    modified_on = moptid_start
                else:
                    modified_on = moptio_start
            else:
                modified_on = segou_start

            Participation.objects.create(
                cluster=routine_cluster,
                entity=entity,
                is_active=True,
                modified_on=modified_on)

            # NIONO, MACINA, MOPTI
            if entity.type.slug == 'health_center' and \
                entity.get_health_district().slug in ('X952', 'TY60', 'HFD9'):

                Participation.objects.create(
                    cluster=routine_cluster_sms,
                    entity=entity,
                    is_active=True,
                    modified_on=modified_on)
