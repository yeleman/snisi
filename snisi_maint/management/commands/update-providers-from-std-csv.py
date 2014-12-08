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
from snisi_tools.auth import create_provider
from snisi_core.models.Entities import Entity
from snisi_core.models.Numbers import PhoneNumber, PhoneNumberType
from snisi_tools.numbers import normalized_phonenumber

if PY2:
    import unicodecsv as csv
else:
    import csv

logger = logging.getLogger(__name__)
gender_map = {"M": Provider.MALE,
              "F": Provider.FEMALE}
title_map = {
    "Mr": Provider.MISTER,
    "Mme": Provider.MISS,
    "Mlle": Provider.MISTRESS,
    "Dr": Provider.DOCTOR,
    "Pr": Provider.PROFESSOR
}


class Command(BaseCommand):

    option_list = BaseCommand.option_list + (
        make_option('-f',
                    help='CSV file',
                    action='store',
                    dest='filename'),
        make_option('-d',
                    help='Enable debug trace',
                    action='store_true',
                    dest='debug'),
    )

    def handle(self, *args, **options):

        if not os.path.exists(options.get('filename') or ""):
            logger.error("CSV file `{}` does not exist."
                         .format(options.get('filename')))
            return

        headers = ['action', 'gender', 'title', 'last_name', 'maiden_name',
                   'first_name', 'other_names', 'role', 'location', 'email',
                   'position', 'flotte', 'orange', 'malitel', 'username',
                   'comment']
        input_csv_file = open(options.get('filename'), 'r')
        csv_reader = csv.DictReader(input_csv_file, fieldnames=headers)

        for entry in csv_reader:
            if csv_reader.line_num == 1:
                continue

            if options.get('debug'):
                logger.debug(entry)

            if entry.get('action') == 'create':
                logger.info("Creating {}".format(entry.get('last_name')))

                first_name = entry.get('first_name') or None
                last_name = entry.get('last_name') or None
                role = entry.get('role') or None
                location = entry.get('location') or None
                email = entry.get('email') or None
                maiden_name = entry.get('maiden_name') or None
                other_names = entry.get('other_names') or None
                gender = gender_map.get(entry.get('gender').upper()) \
                    or Provider.UNKNOWN
                title = title_map.get(entry.get('title')) or None
                position = entry.get('position') or None
                numbers = []
                flotte = entry.get('flotte') or None
                orange = entry.get('orange') or None
                malitel = entry.get('malitel') or None
                if flotte:
                    numbers.append((flotte, True))
                if orange:
                    numbers.append((orange, False))
                if malitel:
                    numbers.append((malitel, False))

                for fv in (first_name, last_name, role, location):
                    if not fv:
                        logger.error("Unable to create Provider. "
                                     "Missing fields?")
                        continue

                p, passwd = create_provider(
                    first_name=first_name,
                    last_name=last_name,
                    role=role,
                    location=location,
                    email=email,
                    middle_name=other_names,
                    maiden_name=maiden_name,
                    gender=gender,
                    title=title,
                    position=position,
                    phone_numbers=numbers)

                logger.info("CREATED,{},{},{}".format(p.username, passwd, p))

            elif entry.get('action') == 'disable':
                p = Provider.get_or_none(entry.get('username'))
                p.is_active = False
                p.save()
                logger.info("DISABLED,{}".format(p))
            elif entry.get('action') == 'move':
                p = Provider.get_or_none(entry.get('username'))
                p.role = Role.get_or_none(entry.get('role'))
                p.location = Entity.get_or_none(entry.get('location'))
                p.save()
                logger.info("MOVED,{}".format(p))
            elif entry.get('action') == 'update':
                p = Provider.get_or_none(entry.get('username'))
                numbers = []
                flotte = entry.get('flotte') or None
                orange = entry.get('orange') or None
                malitel = entry.get('malitel') or None
                if flotte:
                    numbers.append((flotte, True))
                if orange:
                    numbers.append((orange, False))
                if malitel:
                    numbers.append((malitel, False))

                data = {
                    'first_name': entry.get('first_name') or None,
                    'last_name': entry.get('last_name') or None,
                    'role': Role.get_or_none(entry.get('role')) or None,
                    'location':
                        Entity.get_or_none(entry.get('location')) or None,
                    'email': entry.get('email') or None,
                    'maiden_name': entry.get('maiden_name') or None,
                    'middle_name': entry.get('other_names') or None,
                    'gender':
                        gender_map.get(entry.get('gender').upper()) or None,
                    'title': title_map.get(entry.get('title')) or None,
                    'position': entry.get('position') or None
                }

                update = False
                for k, v in data.items():
                    if v is not None:
                        update = True
                        setattr(p, k, v)
                if update:
                    p.save()

                for number, is_flotte in numbers:
                    npn = normalized_phonenumber(number)
                    pnt = PhoneNumberType.from_number(npn, is_flotte=is_flotte)
                    pn = PhoneNumber.get_or_none(npn)
                    if pn is not None:
                        pn.provider = p
                    else:
                        PhoneNumber.objects.create(
                            identity=npn,
                            category=pnt,
                            priority=pnt.priority,
                            provider=p)

                logger.info("UPDATED,{}".format(p))

        logger.info("Done")
