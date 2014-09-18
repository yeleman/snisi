#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim: ai ts=4 sts=4 et sw=4 nu

from __future__ import (unicode_literals, absolute_import,
                        division, print_function)

from django.conf.urls import patterns, url

from snisi_web.url_regexp import (RGXP_ENTITY, RGXP_PERIOD,
                                  RGXP_PERIODS)

urlpatterns = patterns(
    '',

    url(r'^/dashboard/{entity}/{periods}/?$'
        .format(entity=RGXP_ENTITY, periods=RGXP_PERIODS),
        'snisi_reprohealth.views.dashboard.msipf_dashboard',
        name='msipf_dashboard'),
    url(r'^/dashboard/{entity}/?$'.format(entity=RGXP_ENTITY),
        'snisi_reprohealth.views.dashboard.msipf_dashboard',
        name='msipf_dashboard'),
    url(r'^/dashboard/?$',
        'snisi_reprohealth.views.dashboard.msipf_dashboard',
        name='msipf_dashboard'),

    # raw-data browser
    url(r'/{entity}/{period}/?'
        .format(entity=RGXP_ENTITY, period=RGXP_PERIOD),
        'snisi_reprohealth.views.raw_data.browser',
        name='msipf_raw_data'),
    url(r'/{entity}/?'
        .format(entity=RGXP_ENTITY),
        'snisi_reprohealth.views.raw_data.browser',
        {'period_str': None},
        name='msipf_raw_data'),
    url(r'/?',
        'snisi_reprohealth.views.raw_data.browser',
        {'period_str': None, 'entity_slug': None},
        name='msipf_raw_data'),
)
