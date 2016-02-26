#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim: ai ts=4 sts=4 et sw=4 nu

from __future__ import (unicode_literals, absolute_import,
                        division, print_function)

from django.conf.urls import patterns, url

from snisi_web.url_regexp import (RGXP_ENTITY, RGXP_PERIOD,
                                  RGXP_PERIODS, RGXP_RECEIPT)

urlpatterns = patterns(
    '',

    url(r'^/mission/{receipt}?$'
        .format(receipt=RGXP_RECEIPT),
        'snisi_cataract.views.cataract_mission_viewer',
        name='cataract_mission'),

    url(r'^/view/{entity}/{period}/?$'
        .format(entity=RGXP_ENTITY, period=RGXP_PERIOD),
        'snisi_cataract.views.cataract_mission_browser',
        name='cataract_missions'),
    url(r'^/view/{entity}/?$'
        .format(entity=RGXP_ENTITY),
        'snisi_cataract.views.cataract_mission_browser',
        name='cataract_missions'),
    url(r'^/view/?$',
        'snisi_cataract.views.cataract_mission_browser',
        name='cataract_missions'),

    url(r'^/dashboard/{entity}/{periods}/?$'
        .format(entity=RGXP_ENTITY, periods=RGXP_PERIODS),
        'snisi_cataract.views.cataract_dashboard', name='cataract_dashboard'),
    url(r'^/dashboard/{entity}/?$'
        .format(entity=RGXP_ENTITY),
        'snisi_cataract.views.cataract_dashboard', name='cataract_dashboard'),
    url(r'^/dashboard/?$',
        'snisi_cataract.views.cataract_dashboard', name='cataract_dashboard'),
)
