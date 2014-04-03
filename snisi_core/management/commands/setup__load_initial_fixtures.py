#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim: ai ts=4 sts=4 et sw=4 nu

from __future__ import (unicode_literals, absolute_import,
                        division, print_function)

from django.core.management.base import BaseCommand
from django.core.management import call_command


class Command(BaseCommand):

    def handle(self, *args, **options):

        # load safe fixtures
        print(u"Important safe fixtures…")
        call_command("loaddata", "snisi_core/fixtures/Site.xml")
        call_command("loaddata", "snisi_core/fixtures/EntityType.xml")
        call_command("loaddata", "snisi_core/fixtures/Entity-root.xml")
        call_command("loaddata", "snisi_core/fixtures/Role.xml")
        call_command("loaddata", "snisi_core/fixtures/PhoneNumberType.xml")

        call_command("loaddata", "snisi_core/fixtures/AdminUser.xml")
