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

from snisi_core.models.Numbers import PhoneNumberType, PhoneNumber
from snisi_tools.numbers import normalized_phonenumber

if PY2:
    import unicodecsv as csv
else:
    import csv

logger = logging.getLogger(__name__)
flotte = PhoneNumberType.get_or_none('flotte')


def check_number(num):
    if not num:
        return

    norm = normalized_phonenumber(num)
    if not norm:
        return

    pn = PhoneNumber.get_or_none(norm)
    if not pn:
        return

    if pn.category == flotte:
        return

    pn.category = flotte
    pn.priority = flotte.priority
    pn.save()

    return pn


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

        headers = ['num1', 'num2']
        input_csv_file = open(options.get('filename'), 'r')
        csv_reader = csv.DictReader(input_csv_file, fieldnames=headers)

        for entry in csv_reader:
            if csv_reader.line_num == 1:
                continue

            if check_number(entry.get('num1')):
                logger.info(".updated {}".format(entry.get('num1')))
            if check_number(entry.get('num2')):
                logger.info(".updated {}".format(entry.get('num2')))

        logger.info("Done")
