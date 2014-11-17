#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim: ai ts=4 sts=4 et sw=4 nu

from __future__ import (unicode_literals, absolute_import,
                        division, print_function)

from django.conf.urls import patterns, url

from snisi_web.url_regexp import RGXP_ENTITY, RGXP_PERIOD, RGXP_PERIODS

CLUSTER = 'epidemiology_routine'

urlpatterns = patterns(
    '',

    # dashboard
    url(r'^/indicators/{entity}/{periods}/?$'
        .format(entity=RGXP_ENTITY, periods=RGXP_PERIODS),
        'snisi_epidemiology.views.indicators',
        name='epidemio_indicators'),
    url(r'^/indicators/{entity}/?$'
        .format(entity=RGXP_ENTITY),
        'snisi_epidemiology.views.indicators',
        name='epidemio_indicators'),
    url(r'^/indicators/?$',
        'snisi_epidemiology.views.indicators',
        {'template_name': 'epidemiology/indicators.html'},
        name='epidemio_indicators'),
    url(r'^/?$',
        'snisi_epidemiology.views.dashboard',
        {'template_name': 'epidemiology/dashboard_alerts.html'},
        name='epidemio_dashboard'),

    # raw data
    url(r'data/{entity}/{period}/?'
        .format(entity=RGXP_ENTITY, period=RGXP_PERIOD),
        'snisi_web.views.raw_data.browser',
        {'cluster_slug': CLUSTER},
        name='epidemio_raw_data'),
    # Generic report browser without a period
    url(r'data/{entity}/?'
        .format(entity=RGXP_ENTITY),
        'snisi_web.views.raw_data.browser',
        {'cluster_slug': CLUSTER, 'period_str': None},
        name='epidemio_raw_data'),
    url(r'data/?',
        'snisi_web.views.raw_data.browser',
        {'cluster_slug': CLUSTER, 'period_str': None, 'entity_slug': None},
        name='epidemio_raw_data'),
)
