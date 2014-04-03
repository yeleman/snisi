#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim: ai ts=4 sts=4 et sw=4 nu

from __future__ import (unicode_literals, absolute_import,
                        division, print_function)
import logging

from django.core.management.base import BaseCommand

logger = logging.getLogger(__name__)


class Command(BaseCommand):

    def handle(self, *args, **options):

        logger.info("snisi_malaria daily-checkups")

        # create alerts

        # on agg_report (Mali) ready
        # end_of reporting period
        # end_of extended_reporting period
        # auto-validation ? maybe in create_agg
        # end_of district validation period
        # end_of period

        # reminder / every day
        #   1: HC
        #   4: HC
        #   10: district
        #   20: region

        pass
