#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim: ai ts=4 sts=4 et sw=4 nu

from __future__ import (unicode_literals, absolute_import,
                        division, print_function)
import unicodedata

from django.utils import timezone

from snisi_core.models.SMSMessages import SMSMessage


def send_sms(to, text):

    return SMSMessage.objects.create(
        direction=SMSMessage.OUTGOING,
        identity=to,
        event_on=timezone.now(),
        text=text)


def to_ascii(text):
    return unicodedata.normalize('NFKD', unicode(text)) \
                      .encode('ASCII', 'ignore').strip()
