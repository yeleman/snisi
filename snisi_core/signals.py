#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim: ai ts=4 sts=4 et sw=4 nu

from __future__ import (unicode_literals, absolute_import,
                        division, print_function)
import logging

from django.dispatch import Signal


logger = logging.getLogger(__name__)

# forwards django login/logout
logged_in = Signal(providing_args=['provider'])
logged_out = Signal(providing_args=['provider'])

# either though web or sms
changed_passwd = Signal(providing_args=['provider', 'iface'])
edited_profile = Signal(providing_args=['provider', 'iface'])
added_phone = Signal(providing_args=['provider', 'iface'])
removed_phone = Signal(providing_args=['provider', 'iface'])
asked_for_help = Signal(providing_args=['provider', 'iface'])
asked_for_help = Signal(providing_args=['provider', 'iface'])
sent_report_sms = Signal(providing_args=['provider', 'from', 'sms'])
sent_unhandled_sms = Signal(providing_args=['provider', 'from', 'sms'])

uploaded_report = Signal(providing_args=['provider', 'report', 'project'])
edited_report = Signal(providing_args=['provider', 'report', 'project'])
validated_report = Signal(providing_args=['provider', 'report', 'project'])
created_report = Signal(providing_args=['provider', 'report', 'project'])
