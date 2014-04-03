#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim: ai ts=4 sts=4 et sw=4 nu

from __future__ import (unicode_literals, absolute_import,
                        division, print_function)

from django.conf import settings

branding = {
    'brand': "SNISI",
    'brand_short': "SNISI",
    'brand_team': "L'équipe SNISI",
    'brand_full': "Système Numérique d'Information Sanitaire Intégré",
    'hotline': "Hotline SNISI",
    'hotline_num': settings.HOTLINE_NUMBER,
    'hotline_email': settings.HOTLINE_EMAIL,
}

branding.update({
    'notification_from': "Notifications SNISI <{email}>".format(
        email=settings.HOTLINE_EMAIL)
})
