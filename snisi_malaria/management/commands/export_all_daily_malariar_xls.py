#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim: ai ts=4 sts=4 et sw=4 nu

from __future__ import (unicode_literals, absolute_import,
                        division, print_function)
import logging
import os

from django.core.management.base import BaseCommand
from optparse import make_option

from snisi_malaria.xls_export import all_daily_malariar_as_xls

logger = logging.getLogger(__name__)


class Command(BaseCommand):

    option_list = BaseCommand.option_list + (
        make_option('-p',
                    help='Path (file) to export xls file to',
                    action='store',
                    dest='xls_path'),
    )

    def handle(self, *args, **options):
        dest = options.get('xls_path')
        if not dest:
            logger.error("You must specify xls destination")
            return
        all_daily_malariar_as_xls(save_to=options.get('xls_path'))
