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

from snisi_core.models.Entities import Entity, HealthEntity, EntityType
from snisi_core.models.Roles import Role
from snisi_core.models.Providers import Provider
from snisi_core.models.Projects import Cluster, Participation
from snisi_core.models.Reporting import ExpectedReporting, ReportClass
from snisi_tools.auth import create_provider
from snisi_reprohealth.models.PFActivities import (
    AggPFActivitiesR, PFActivitiesR)

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

        cluster = Cluster.get_or_none('msi_reprohealth_routine')
        cluster_sms = Cluster.get_or_none('msi_reprohealth_routine_sms')

        if not os.path.exists(options.get('filename') or ""):
            logger.error("CSV file `{}` does not exist."
                         .format(options.get('filename')))
            return

        # delete existing expected and PFActivitiesR
        if False:
            for rc in ('msi_pf_monthly_routine',
                       'msi_pf_monthly_routine_aggregated'):
                ExpectedReporting.objects.filter(
                    report_class=ReportClass.get_or_none(rc)).delete()
            PFActivitiesR.objects.all().delete()
            AggPFActivitiesR.objects.all().delete()

        privates = {
            'PTAP9': ('ZX5W9', "Cabinet Liberté"),
            'PK9J0': ('ZKTE4', "Cabinet Medical Tama"),
            'PEWA3': ('ZNZC8', "Clinique Lafia"),
            'PB550': ('ZNZC8', "Cabinet Tata SYLLA"),
            'PYZ49': (None, "Cabinet Satis-Santé"),
            'P2DY1': ('Z4622', "Cabinet Bonté"),
            'PXDF7': ('ZPSS1', "Cabinet Espoir")
        }

        headers = [
            'Genre', 'Titre', 'Nom', 'Nomdejeune-fille', 'Prenom',
            'Autresprenom', 'email', 'Role', 'Localite', 'Fonction',
            'Flotte', 'Orange', 'Malitel', 'Username', 'comment']
        input_csv_file = open(options.get('filename'), 'r')
        csv_reader = csv.DictReader(input_csv_file, fieldnames=headers)

        private_type = EntityType.get_or_none('private')

        new_users = []

        for entry in csv_reader:
            if csv_reader.line_num == 1:
                continue

            if not entry.get('Nom').strip():
                continue

            entity_code = entry.get('Localite').strip().upper()

            if len(entity_code) == 5 and entity_code.startswith('P'):
                ha_slug, name = privates.get(entity_code)
                if ha_slug is None:
                    # Ouinzinbougou Satis-santé
                    continue

                entity = HealthEntity.objects.create(
                    slug=entity_code,
                    name=name,
                    type=private_type,
                    parent=Entity.get_or_none(ha_slug))
            else:
                entity = Entity.get_or_none(entry.get('Localite'))

            if entity is None:
                logger.warning("Entity `{}` does not exist."
                               .format(entry.get('Localite')))
                break

            role = Role.get_or_none(entry.get('Role').lower())
            if role is None:
                logger.warning("Role `{}` does not exist."
                               .format(entry.get('Role')))
                break

            genders = {
                'M': Provider.MALE,
                'F': Provider.FEMALE
            }

            titles = {
                'M.': Provider.MISTER,
                'Mlle': Provider.MISTRESS,
                'Dr': Provider.DOCTOR,
                'DR': Provider.DOCTOR,
                'Mme': Provider.MISS
            }

            first_name = entry.get('Prenom') or "Mamadou"
            last_name = entry.get('Nom')
            gender = genders.get(entry.get('Genre'))
            title = titles.get(entry.get('Titre') or 'M.')
            maiden_name = entry.get('Nomdejeune-fille') or None
            other_names = entry.get('Autresprenom') or None
            email = entry.get('email') or None
            position = entry.get('Fonction') or None
            flotte_number = entry.get('Flotte') or None
            orange_number = entry.get('Orange') or None
            malitel_number = entry.get('Malitel') or None

            numbers = []
            if flotte_number:
                numbers.append((flotte_number, True))
            if orange_number:
                numbers.append((orange_number, False))
            if malitel_number:
                numbers.append((malitel_number, False))

            username = entry.get('Username').strip()
            if username:
                provider = Provider.get_or_none(username)
                logger.info("Provider {} already exist.".format(provider))
            else:
                provider, passwd = create_provider(
                    first_name=first_name,
                    last_name=last_name,
                    role=role.slug,
                    location=entity.slug,
                    email=email,
                    middle_name=other_names,
                    maiden_name=maiden_name,
                    gender=gender,
                    title=title,
                    position=position,
                    phone_numbers=numbers)
                logger.info("Created Provider {}.".format(provider))
                new_users.append((provider, passwd))

            p, created = Participation.objects.get_or_create(
                cluster=cluster,
                entity=entity,
                is_active=True)
            if created:
                logger.info("Add {} to Cluster {}".format(entity, cluster))

            p, created = Participation.objects.get_or_create(
                cluster=cluster_sms,
                entity=entity,
                is_active=True)
            if created:
                logger.info("Add {} to Cluster {}".format(entity, cluster))

        print("\n".join(["{},{},{}".format(pr, pr.username, pw)
                         for pr, pw in new_users]))
