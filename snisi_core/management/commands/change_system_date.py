#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim: ai ts=4 sts=4 et sw=4 nu

from __future__ import (unicode_literals, absolute_import,
                        division, print_function)
import datetime

from optparse import make_option
from django.core.management.base import BaseCommand

from snisi_tools.datetime import DEBUG_change_system_date


class Command(BaseCommand):

    option_list = BaseCommand.option_list + (
        make_option('-d',
                    help='Date to change to: YYYY-MM-DD or auto',
                    action='store',
                    dest='input_date'),
        )

    def handle(self, *args, **options):
        date_str = options.get('input_date').lower()
        if not date_str == 'auto':
            new_date = datetime.datetime(*[int(e) for e in date_str.split('-')])
        else:
            new_date = None

        DEBUG_change_system_date(new_date, True)
