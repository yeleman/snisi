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

from snisi_core.models.Providers import Provider
from snisi_core.models.Roles import Role
from snisi_core.models.Entities import Entity
from snisi_tools.auth import create_provider

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

        headers = ['Genre', 'Titre', 'Nom', 'Nomdejeune-fille', 'Prenom',
                   'Autresprenom', 'email', 'Role', 'Localite',
                   'Fonction', 'Flotte', 'Orange', 'Malitel',
                   'Username', 'comment']

        created = []

        input_csv_file = open(options.get('filename'), 'r')
        csv_reader = csv.DictReader(input_csv_file, fieldnames=headers)

        for entry in csv_reader:
            if csv_reader.line_num == 1:
                continue

            username = entry.get('Username')
            if username:
                # update user ?
                provider = Provider.get_or_none(username)
                logger.info("Updating {}".format(provider))
            else:
                gender = Provider.FEMALE \
                    if entry.get('Genre').strip().upper() == "f" \
                    else Provider.MALE

                titles = {
                    "Mme": Provider.MISS,
                    "Dr": Provider.DOCTOR,
                    "M.": Provider.MISTER,
                    "Mlle": Provider.MISTRESS
                }
                title = titles.get(entry.get('Titre'))

                last_name = entry.get('Nom') or None
                first_name = entry.get('Prenom') or None
                maiden_name = entry.get('Nomdejeune-fille') or None
                maiden_name = entry.get('Nomdejeune-fille') or None
                other_name = entry.get('Autresprenom') or None
                email = entry.get('email') or None
                role = Role.get_or_none(entry.get('Role'))
                entity = Entity.get_or_none(entry.get('Localite'))
                orange = entry.get('Orange') or None
                malitel = entry.get('Malitel') or None
                numbers = []
                if orange:
                    numbers.append(orange)
                if malitel:
                    numbers.append(malitel)

                provider, passwd = create_provider(
                    first_name=first_name,
                    last_name=last_name,
                    role=role.slug,
                    location=entity.slug,
                    email=email,
                    middle_name=other_name,
                    maiden_name=maiden_name,
                    gender=gender,
                    title=title,
                    phone_numbers=numbers)
                provider.set_password("aaaa")
                provider.save()
                created.append(provider)

                logger.info("Created {}".format(provider))

        logger.info("Done")

        created_str = "\n".join([p.username for p in created])
        print(created_str)
        with open('created.txt', 'w') as f:
            f.write(created_str)
