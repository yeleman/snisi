#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim: ai ts=4 sts=4 et sw=4 nu

from __future__ import (unicode_literals, absolute_import,
                        division, print_function)

from django.conf import settings
from django.conf.urls import patterns, url


urlpatterns = patterns('',
    url(r'^map/?$',
        'snisi_vacc.views.vacc_map',
        {'template_name': 'vaccination/map.html'},
        name='vacc_map'),
)
