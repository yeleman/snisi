#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim: ai ts=4 sts=4 et sw=4 nu

from __future__ import (unicode_literals, absolute_import,
                        division, print_function)

from django.conf import settings
from django.conf.urls import patterns, url
from django.conf.urls.static import static
from django.views.generic.base import TemplateView
from django.http import HttpResponse

RGXP_REPORTCLS = r'(?P<reportcls_slug>[a-zA-Z\_\-0-1]+)'
RGXP_CLUSTER = r'(?P<cluster_slug>[a-zA-Z\_\-0-1\-]+)'
RGXP_ENTITY = r'(?P<entity_slug>[a-zA-Z0-9]+)'
RGXP_RECEIPT = r'(?P<report_receipt>[a-zA-Z\#\-\_\.0-9\/]+)'
RGXP_SECTION = 'section(?P<section_index>[0-9]{1,2}[ab]{0,1})'
RGXP_SUBSECTION = '(?P<sub_section>[a-z\_]*)'

"""
FORMATS:

YEAR:       2013                                [0-9]{4}
MONTH:      01-2013                             [0-9]{2}-[0-9]{4}
QUARTER:    Q1-2013                             Q[1-3]-[0-9]{4}
WEEK:       W1-2013                             W[0-9]{1,2}-[0-9]{4}
DAY:        01-01-2013                          [0-9]{2}-[0-9]{2}-[0-9]{4}
"""
RGXP_PERIOD = r'(?P<period_str>[0-9]{4}|[0-9]{2}\-[0-9]{4}|Q[1-3]\-[0-9]{4}|W[0-9]{1,2}\-[0-9]{4}|[0-9]{2}\-[0-9]{2}\-[0-9]{4})/?$'

RGXP_PERIODS = (r'(?P<period_str>'
                r'[0-9]{4}|[0-9]{2}\-[0-9]{4}|Q[1-3]\-[0-9]{4}|'
                r'W[0-9]{1,2}\-[0-9]{4}|[0-9]{2}\-[0-9]{2}\-[0-9]{4}'
                r'_'
                r'[0-9]{4}|[0-9]{2}\-[0-9]{4}|Q[1-3]\-[0-9]{4}|'
                r'W[0-9]{1,2}\-[0-9]{4}|[0-9]{2}\-[0-9]{2}\-[0-9]{4}'
                r')')

RGXP_PERIODS = r'(?P<perioda_str>[0-9]{4}|[0-9]{2}\-[0-9]{4}|Q[1-3]\-[0-9]{4}|W[0-9]{1,2}\-[0-9]{4}|[0-9]{2}\-[0-9]{2}\-[0-9]{4})_(?P<periodb_str>[0-9]{4}|[0-9]{2}\-[0-9]{4}|Q[1-3]\-[0-9]{4}|W[0-9]{1,2}\-[0-9]{4}|[0-9]{2}\-[0-9]{2}\-[0-9]{4})'

urlpatterns = patterns('',

    url(r'^download/(?P<fpath>.*)$',
        'snisi_web.views.downloads.serve_protected_files', name='protected'),

    # authentication
    url(r'^login/$', 'django.contrib.auth.views.login',
        {'template_name': 'misc/login.html'}, name='login'),
    url(r'^logout/$', 'django.contrib.auth.views.logout',
        {'next_page': '/'}, name='logout'),

    # Android API
    url(r'^fondasms/?$', 'fondasms.views.fondasms_handler',
        {'handler_module': 'snisi_sms.fondasms_handlers',
         'send_automatic_reply': False,
         'automatic_reply_via_handler': False,
         'automatic_reply_text': None},
        name='fondasms'),
    url(r'^fondasms/test/?$',
        TemplateView.as_view(template_name="fondasms_tester.html"),
        name='fondasms_tester'),


    # SNISI
    url(r'^$', 'snisi_web.views.dashboard.user_dashboard', name='home'),
    url(r'^upload$', 'snisi_web.views.upload.upload_form', name='upload'),
    url(r'^validation/' + RGXP_RECEIPT +'/do$', 'snisi_web.views.validation.do_validation', name='validation_do_validate'),
    url(r'^validation/' + RGXP_RECEIPT +'$', 'snisi_web.views.validation.edit_report', name='validation_edit'),
    url(r'^validation$', 'snisi_web.views.validation.pending_validation_list', name='validation'),
    url(r'^addressbook$', 'snisi_web.views.addressbook.addressbook', name='addressbook'),
    url(r'^monitoring/periodic$',
        'snisi_web.views.monitoring.periodic_sources.periodic_source_dashboard',
        name='periodic_source_monitoring'),

    # Entities API
    url(r'^api/entities/getchildren/(?P<parent_slug>[A-Za-z0-9\_]{3,4})/(?P<type_slug>[a-zA-Z0-9\-\_]+)/?$',
        'snisi_web.views.entities_api.get_children', name='api_entities_get_children'),

    url(r'^api/entities/getclusterchildren/(?P<cluster_slug>[A-Za-z0-9\_\-]+)/(?P<parent_slug>[A-Za-z0-9\_]{3,4})/(?P<type_slug>[a-zA-Z0-9\-\_]+)/?$',
        'snisi_web.views.entities_api.get_cluster_children', name='api_entities_get_cluster_children'),

    url(r'^api/entities/get_epidemio_children/(?P<parent_slug>[A-Za-z0-9\_]{3,4})/(?P<type_slug>[a-zA-Z0-9\-\_]+)/?$',
        'snisi_web.views.entities_api.get_epidemio_children', name='api_entities_get_epidemio_children'),

    # Malaria GeoJSON
    url(r'^api/malaria/geojson/(?P<parent_slug>[a-zA-Z0-9]+)?$',
        'snisi_malaria.views.mapping.geojson_data', name='malaria_geojson_data'),
     url(r'^api/malaria/indicators/?$',
        'snisi_malaria.views.mapping.get_indicator_data', name='malaria_indicator'),

    url(r'^api/indicators/geo/?$',
        'snisi_web.views.indicators_api.geojson_indicator', name='geojson_indicator'),

    # Indicators API
    url(r'^api/indicators/(?P<key>[a-zA-Z0-9\_]*)/?$',
        'snisi_web.views.indicators_api.list_all_indicators', name='api_indicators'),


    # Generic raw-data browser
    url(r'data/{cluster}/{entity}/{period}/?'.format(
            cluster=RGXP_CLUSTER, entity=RGXP_ENTITY, period=RGXP_PERIOD),
        'snisi_web.views.raw_data.browser', name='report_browser'),
    # Generic report browser without a period
    url(r'data/{cluster}/{entity}/?'.format(
            cluster=RGXP_CLUSTER, entity=RGXP_ENTITY),
        'snisi_web.views.raw_data.browser', {'period_str': None}, name='report_browser_noperiod'),

    # Custom indicator (section 13)
    url(r'^malaria/view/custom?$',
        'snisi_malaria.views.indicators.custom_indicator',
        name='malaria_custom'),

     # Malaria Indicator Browser
    url(r'^malaria/rtf/{entity}/{periods}/{section}/{subsection}/?$'
        .format(entity=RGXP_ENTITY, periods=RGXP_PERIODS,
                section=RGXP_SECTION, subsection=RGXP_SUBSECTION),
        'snisi_malaria.views.indicators.export', name='malaria_section_rtf_export'),
    url(r'^malaria/view/{entity}/{periods}/{section}/{subsection}/?$'
        .format(entity=RGXP_ENTITY, periods=RGXP_PERIODS,
                section=RGXP_SECTION, subsection=RGXP_SUBSECTION),
        'snisi_malaria.views.indicators.browser', name='malaria_view'),
    url(r'^malaria/view/{entity}/{periods}/{section}/?$'
        .format(entity=RGXP_ENTITY, periods=RGXP_PERIODS,
                section=RGXP_SECTION),
        'snisi_malaria.views.indicators.browser', name='malaria_view'),
    url(r'^malaria/view/{entity}/{periods}/?$'
        .format(entity=RGXP_ENTITY, periods=RGXP_PERIODS),
        'snisi_malaria.views.indicators.browser', name='malaria_view'),
    url(r'^malaria/view/{entity}/?$'
        .format(entity=RGXP_ENTITY),
        'snisi_malaria.views.indicators.browser', name='malaria_view'),
    url(r'^malaria/view/?$', 'snisi_malaria.views.indicators.browser'
        .format(),
        name='malaria_view'),


    url(r'^malaria/epidemio/{entity}/{periods}/?$'
        .format(entity=RGXP_ENTITY, periods=RGXP_PERIODS),
        'snisi_malaria.views.epidemio.display_epidemio', name='malaria_epidemio'),
    url(r'^malaria/epidemio/{entity}/?$'
        .format(entity=RGXP_ENTITY),
        'snisi_malaria.views.epidemio.display_epidemio', name='malaria_epidemio'),
    url(r'^malaria/epidemio/?$',
        'snisi_malaria.views.epidemio.display_epidemio', name='malaria_epidemio'),


    # quarter reports
    url(r'^malaria/quarter-reports/'+RGXP_ENTITY+'/?$',
        'snisi_malaria.views.quarter_reports.display_report',
        name='malaria_quarter_report'),
    url(r'^malaria/quarter-reports/?$',
        'snisi_malaria.views.quarter_reports.display_report',
        name='malaria_quarter_report'),


    url(r'download-report/{receipt}.xls'.format(receipt=RGXP_RECEIPT),
        'snisi_web.views.raw_data.download_as_excel',
        name='download_report_xls'),

    url(r'map/malaria/?$',
        'snisi_malaria.views.mapping.malaria_map',
        {'template_name': 'malaria/map.html'},
        name='malaria_map'),

    url(r'map/{reportcls}/?'.format(
            reportcls=RGXP_REPORTCLS),
        'snisi_web.views.mapping.webmap', name='map'),

    # Trachoma
    url(r'^trachoma/mission/{receipt}?$'.format(receipt=RGXP_RECEIPT),
        'snisi_trachoma.views.trachoma_mission_viewer', name='trachoma_mission'),

    url(r'^trachoma/view/{entity}/{period}/?$'
        .format(entity=RGXP_ENTITY, period=RGXP_PERIOD),
        'snisi_trachoma.views.trachoma_mission_browser', name='trachoma_missions'),
    url(r'^trachoma/view/{entity}/?$'
        .format(entity=RGXP_ENTITY),
        'snisi_trachoma.views.trachoma_mission_browser', name='trachoma_missions'),
    url(r'^trachoma/view/?$',
        'snisi_trachoma.views.trachoma_mission_browser', name='trachoma_missions'),

    url(r'^trachoma/dashboard/{entity}/{periods}/?$'
        .format(entity=RGXP_ENTITY, periods=RGXP_PERIODS),
        'snisi_trachoma.views.trachoma_dashboard', name='trachoma_dashboard'),
    url(r'^trachoma/dashboard/{entity}/?$'
        .format(entity=RGXP_ENTITY),
        'snisi_trachoma.views.trachoma_dashboard', name='trachoma_dashboard'),
    url(r'^trachoma/dashboard/?$',
        'snisi_trachoma.views.trachoma_dashboard', name='trachoma_dashboard'),

    # CSN
    url(r'^entities/' + RGXP_ENTITY + '/?$',
        'snisi_web.views.entities.entity_profile',
        {'template_name': 'misc/entity_profile.html'},
        name='entity_profile'),
    url(r'^entities/?$',
        'snisi_web.views.entities.entities_list',
        {'template_name': 'misc/entities_list.html'},
        name='entities_list'),

    # User profile
    url(r'^myprofile/?$',
        'snisi_web.views.providers.edit_profile',
        {'template_name': 'misc/edit_profile.html'},
        name='profile'),
    url(r'^myprofile/delete-num/(?P<identity>[\+0-9]+)/?$',
        'snisi_web.views.providers.remove_number_from_profile',
        name='profile-remove-number'),
    url(r'^~(?P<username>[a-zA-Z0-9\_\-]+)/?$',
        'snisi_web.views.providers.public_profile',
        {'template_name': 'misc/public_profile.html'},
        name='public_profile'),

    # misclaneous
    url(r'^about/?$',
        TemplateView.as_view(template_name='misc/about.html'),
        name='about'),
    url(r'^support/?$',
        TemplateView.as_view(template_name='misc/support.html'),
        name='support'),
    url(r'^contact/?$',
        'snisi_web.views.misc.contact',
        {'template_name': 'misc/contact.html'},
        name='contact'),


    # resources view to be override by httpd
    url(r'^resources/?$',
        lambda x: HttpResponse('Resources Unavailable'),
        name='resources'),

) + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
