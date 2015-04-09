#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim: ai ts=4 sts=4 et sw=4 nu

from __future__ import (unicode_literals, absolute_import,
                        division, print_function)
import logging

from django.core.management.base import BaseCommand
from django.contrib.sessions.models import Session
from optparse import make_option

logger = logging.getLogger(__name__)


class Command(BaseCommand):

    option_list = BaseCommand.option_list + (
        make_option('-s',
                    help='Session Key',
                    action='store',
                    dest='session_key'),
    )

    def handle(self, *args, **options):

        if not options.get('session_key'):
            logger.error("No session key provided")
            return

        try:
            session = Session.objects.get(
                session_key=options.get('session_key'))
        except Session.DoesNotExist:
            logger.error("Invalid session key: Does Not Exist.")
            return

        logger.info(session.get_decoded())
