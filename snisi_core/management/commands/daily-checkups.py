#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim: ai ts=4 sts=4 et sw=4 nu

from __future__ import (unicode_literals, absolute_import,
                        division, print_function)
import logging

from django.core.management.base import BaseCommand
from django.core.management import call_command

from snisi_core.models.Projects import Domain

logger = logging.getLogger(__name__)


class Command(BaseCommand):

    def handle(self, *args, **options):

        logger.info("Running daily checkups for all apps")

        for domain in Domain.active.all():

            if domain.import_from('management.commands.{}_daily'
                                  .format(domain.module_path)) is not None:
                cmd = "{}_daily".format(domain.module_path)
                try:
                    logger.info("Running {}".format(cmd))
                    call_command(cmd)
                except Exception as exp:
                    logger.error("Caught an exception while running daily command")
                    logger.error(exp)
                    continue

        logger.info("End of daily checkups.")

