#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim: ai ts=4 sts=4 et sw=4 nu

from __future__ import (unicode_literals, absolute_import,
                        division, print_function)
import logging
import datetime

from django.core.management.base import BaseCommand
from django.utils import timezone

from snisi_core.models.SMSMessages import SMSMessage
from snisi_sms.handler import snisi_sms_handler

logger = logging.getLogger(__name__)


class Command(BaseCommand):

    def handle(self, *args, **options):

        now = timezone.now()
        limit = now - datetime.timedelta(days=5)

        for msg in SMSMessage.objects.filter(
                direction=SMSMessage.INCOMING,
                handled=False,
                created_on__gte=limit):

            msg_id = msg.id
            if snisi_sms_handler(msg):
                # we re-get the message from the DB
                # since handlers are allowed to destroy it (spam, etc)
                try:
                    msg = SMSMessage.objects.get(id=msg_id)
                except SMSMessage.DoesNotExist:
                    pass
                # might already be marked handled
                else:
                    if not msg.handled:
                        msg.handled = True
                        msg.save()
