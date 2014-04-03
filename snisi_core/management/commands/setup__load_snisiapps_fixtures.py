#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim: ai ts=4 sts=4 et sw=4 nu

from __future__ import (unicode_literals, absolute_import,
                        division, print_function)
import os

from django.core.management.base import BaseCommand
from django.core.management import call_command
from django.conf import settings


class Command(BaseCommand):

    def handle(self, *args, **options):

        print(u"SNISI Apps fixtures…")

        for app in settings.INSTALLED_APPS:
            if not app.startswith('snisi_') or app in ('snisi_core',
                                                       'snisi_web',
                                                       'snisi_tools',
                                                       'snisi_sms'):
                continue
            dname = os.path.join(app, "fixtures")
            if not os.path.exists(dname):
                continue
            for fname in os.listdir(dname):
                if not fname.endswith('.xml'):
                    continue
                call_command("loaddata", os.path.join(dname, fname))
