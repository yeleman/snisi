#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim: ai ts=4 sts=4 et sw=4 nu

from __future__ import (unicode_literals, absolute_import,
                        division, print_function)

from django.conf.urls import patterns, url

from snisi_web.url_regexp import RGXP_ENTITY, RGXP_PERIOD, RGXP_PERIODS

urlpatterns = patterns(
    '',

    url(r'^/dashboard/?$', 'snisi_nutrition.views.indicators.dashboard',
        name='nutrition_dashboard'),

    # weekly nutrition
    url(r'^/weekly/{entity}/{periods}/?$'
        .format(entity=RGXP_ENTITY, periods=RGXP_PERIODS),
        'snisi_nutrition.views.weekly.display_weekly',
        name='nutrition_weekly'),
    url(r'^/weekly/{entity}/?$'
        .format(entity=RGXP_ENTITY),
        'snisi_nutrition.views.weekly.display_weekly',
        name='nutrition_weekly'),
    url(r'^/weekly/?$',
        'snisi_nutrition.views.weekly.display_weekly',
        name='nutrition_weekly'),

    # indicator browser
    url(r'^/view/{entity}/{periods}/?$'
        .format(entity=RGXP_ENTITY, periods=RGXP_PERIODS),
        'snisi_nutrition.views.indicators.browser', name='nutrition_view'),
    url(r'^/view/{entity}/?$'
        .format(entity=RGXP_ENTITY),
        'snisi_nutrition.views.indicators.browser', name='nutrition_view'),
    url(r'^/view/?$', 'snisi_nutrition.views.indicators.browser'
        .format(),
        name='nutrition_view'),

    # raw-data browser
    url(r'/{entity}/{period}/?'
        .format(entity=RGXP_ENTITY, period=RGXP_PERIOD),
        'snisi_nutrition.views.raw_data.browser',
        name='nutrition_raw_data'),
    url(r'/{entity}/?'
        .format(entity=RGXP_ENTITY),
        'snisi_nutrition.views.raw_data.browser',
        {'period_str': None},
        name='nutrition_raw_data'),
    url(r'/?',
        'snisi_nutrition.views.raw_data.browser',
        {'period_str': None, 'entity_slug': None},
        name='nutrition_raw_data'),
)
