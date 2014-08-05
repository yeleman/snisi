#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim: ai ts=4 sts=4 et sw=4 nu

from __future__ import (unicode_literals, absolute_import,
                        division, print_function)

from django.conf.urls import patterns, url

from snisi_web.url_regexp import (RGXP_ENTITY, RGXP_PERIODS,
                                  RGXP_SECTION, RGXP_SUBSECTION)

urlpatterns = patterns(
    '',

    # Custom indicator (section 13)
    url(r'^/view/custom?$',
        'snisi_malaria.views.indicators.custom_indicator',
        name='malaria_custom'),

    # Malaria Indicator Browser
    url(r'^/rtf/{entity}/{periods}/{section}/{subsection}/?$'
        .format(entity=RGXP_ENTITY, periods=RGXP_PERIODS,
                section=RGXP_SECTION, subsection=RGXP_SUBSECTION),
        'snisi_malaria.views.indicators.export',
        name='malaria_section_rtf_export'),
    url(r'^/view/{entity}/{periods}/{section}/{subsection}/?$'
        .format(entity=RGXP_ENTITY, periods=RGXP_PERIODS,
                section=RGXP_SECTION, subsection=RGXP_SUBSECTION),
        'snisi_malaria.views.indicators.browser', name='malaria_view'),
    url(r'^/view/{entity}/{periods}/{section}/?$'
        .format(entity=RGXP_ENTITY, periods=RGXP_PERIODS,
                section=RGXP_SECTION),
        'snisi_malaria.views.indicators.browser', name='malaria_view'),
    url(r'^/view/{entity}/{periods}/?$'
        .format(entity=RGXP_ENTITY, periods=RGXP_PERIODS),
        'snisi_malaria.views.indicators.browser', name='malaria_view'),
    url(r'^/view/{entity}/?$'
        .format(entity=RGXP_ENTITY),
        'snisi_malaria.views.indicators.browser', name='malaria_view'),
    url(r'^/view/?$', 'snisi_malaria.views.indicators.browser'
        .format(),
        name='malaria_view'),

    # weekly malaria epidemio
    url(r'^/epidemio/{entity}/{periods}/?$'
        .format(entity=RGXP_ENTITY, periods=RGXP_PERIODS),
        'snisi_malaria.views.epidemio.display_epidemio',
        name='malaria_epidemio'),
    url(r'^/epidemio/{entity}/?$'
        .format(entity=RGXP_ENTITY),
        'snisi_malaria.views.epidemio.display_epidemio',
        name='malaria_epidemio'),
    url(r'^/epidemio/?$',
        'snisi_malaria.views.epidemio.display_epidemio',
        name='malaria_epidemio'),


    # quarter reports
    url(r'^/quarter-reports/'+RGXP_ENTITY+'/?$',
        'snisi_malaria.views.quarter_reports.display_report',
        name='malaria_quarter_report'),
    url(r'^/quarter-reports/?$',
        'snisi_malaria.views.quarter_reports.display_report',
        name='malaria_quarter_report'),
)
