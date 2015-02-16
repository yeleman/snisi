#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim: ai ts=4 sts=4 et sw=4 nu

from __future__ import (unicode_literals, absolute_import,
                        division, print_function)
import logging
import os

from django.core.management.base import BaseCommand
from django.core.management import call_command
from optparse import make_option

from snisi_core.models.Projects import Domain

logger = logging.getLogger(__name__)


class Command(BaseCommand):

    option_list = BaseCommand.option_list + (
        make_option('--update',
                    help='Update .po files',
                    action='store_true',
                    dest='update'),
        make_option('--compile',
                    help='Compile .po files into .mo files',
                    action='store_true',
                    dest='compile'),
    )

    def handle(self, *args, **options):

        domains = [domain.module_path for domain in Domain.active.all()] + \
            ['snisi_web', 'snisi_core', 'snisi_sms', 'snisi_tools']

        root = os.getcwdu()

        if options.get('update'):
            logger.info("Updating PO files…")

            for domain in domains:
                if not os.path.exists(os.path.join(domain, 'locale')):
                    continue

                logger.info("..{}".format(domain))

                os.chdir(domain)
                call_command("makemessages", locale=["fr"])
                os.chdir(root)

            os.chdir(root)

        if options.get('compile'):
            logger.info("Compiling MO files…")

            for domain in domains:
                if not os.path.exists(os.path.join(domain, 'locale')):
                    continue

                logger.info("..{}".format(domain))

                os.chdir(domain)
                call_command("compilemessages", locale=["fr"])
                os.chdir(root)

            os.chdir(root)
