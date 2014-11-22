#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim: ai ts=4 sts=4 et sw=4 nu

from __future__ import (unicode_literals, absolute_import,
                        division, print_function)
import logging

from django.core.management.base import BaseCommand

from snisi_core.models.Providers import Provider

logger = logging.getLogger(__name__)


class Command(BaseCommand):

    def handle(self, *args, **options):

        usernames = ['kdembel1', 'ldiabat', 'adougnon', 'sdoumbi1',
                     'dguindo', 'amaiga2', 'sombotem']

        for username in usernames:
            p = Provider.get_or_none(username)
            logger.info("Deleting {}".format(p))
            p.delete()
