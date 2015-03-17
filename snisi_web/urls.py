#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim: ai ts=4 sts=4 et sw=4 nu

from __future__ import (unicode_literals, absolute_import,
                        division, print_function)

from django.conf import settings
from django.conf.urls import patterns, url, include
from django.conf.urls.static import static
from django.views.generic.base import TemplateView
from django.http import HttpResponse

from snisi_web.url_regexp import (RGXP_ENTITY,
                                  RGXP_RECEIPT,
                                  RGXP_PERIOD)
from snisi_malaria import urls as malaria_urls
from snisi_vacc import urls as vacc_urls
from snisi_epidemiology import urls as epidemio_urls
from snisi_reprohealth import urls as reprohealth_urls
from snisi_nutrition import urls as nutrition_urls
from snisi_trachoma import urls as trachoma_urls

urlpatterns = patterns(
    '',

    url(r'^malaria', include(malaria_urls)),
    url(r'^nutrition', include(nutrition_urls)),
    url(r'^vaccination', include(vacc_urls)),
    url(r'^msi_pf', include(reprohealth_urls)),
    url(r'^epidemiology', include(epidemio_urls)),
    url(r'^trachoma', include(trachoma_urls)),

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

    # Admin pages
    url(r'^admin/add_provider/?$',
        'snisi_web.views.admin.add_provider',
        {'template_name': 'admin/add_provider.html'},
        name='admin_add_provider'),
    url(r'^admin/reset_password/(?P<username>[a-zA-Z0-9\_\-]+)?$',
        'snisi_web.views.admin.reset_password',
        name='admin_reset_password'),
    url(r'^admin/disable_provider/(?P<username>[a-zA-Z0-9\_\-]+)?$',
        'snisi_web.views.admin.disable_provider',
        name='admin_disable_provider'),
    url(r'^admin/enable_provider/(?P<username>[a-zA-Z0-9\_\-]+)?$',
        'snisi_web.views.admin.enable_provider',
        name='admin_enable_provider'),
    url(r'^admin/phone-numbers/?$',
        'snisi_web.views.admin.find_phonenumber',
        {'template_name': 'admin/find_phonenumber.html'},
        name='admin_find_phonenumber'),
    url(r'^admin/phone-numbers/(?P<identity>[0-9\+]+)/delete/?$',
        'snisi_web.views.admin.delete_phonenumber',
        name='admin_delete_phonenumber'),


    # SNISI
    url(r'^$', 'snisi_web.views.dashboard.user_dashboard', name='home'),
    url(r'^upload$', 'snisi_web.views.upload.upload_form', name='upload'),
    url(r'^validation/' + RGXP_RECEIPT + '/do$',
        'snisi_web.views.validation.do_validation',
        name='validation_do_validate'),
    url(r'^validation/' + RGXP_RECEIPT + '$',
        'snisi_web.views.validation.edit_report',
        name='validation_edit'),
    url(r'^validation$',
        'snisi_web.views.validation.pending_validation_list',
        name='validation'),
    url(r'^addressbook$',
        'snisi_web.views.addressbook.addressbook',
        name='addressbook'),
    url(r'^monitoring/periodic$',
        'snisi_web.views.monitoring.periodic_sources.'
        'periodic_source_dashboard',
        name='periodic_source_monitoring'),

    # Entities API
    url(r'^api/entity/'
        '(?P<entity_slug>[A-Za-z0-9\_]{3,4})/?$',
        'snisi_web.views.entities_api.get_detail',
        name='api_entity_detail'),

    url(r'^api/entities/getchildren/'
        '(?P<parent_slug>[A-Za-z0-9\_]{3,4})'
        '/(?P<type_slug>[a-zA-Z0-9\-\_]+)/?$',
        'snisi_web.views.entities_api.get_children',
        name='api_entities_get_children'),

    url(r'^api/entities/getclusterchildren/'
        '(?P<cluster_slug>[A-Za-z0-9\_\-]+)'
        '/(?P<parent_slug>[A-Za-z0-9\_]{3,4})'
        '/(?P<type_slug>[a-zA-Z0-9\-\_]+)/?$',
        'snisi_web.views.entities_api.get_cluster_children',
        name='api_entities_get_cluster_children'),

    # GeoJSON API
    url(r'^api/geojson/(?P<cluster_slug>[a-z0-9\-\_]+)/'
        '(?P<parent_slug>[a-zA-Z0-9]+)?$',
        'snisi_web.views.mapping.geojson_data',
        name='api_geojson_data'),

    url(r'^api/(?P<domain_slug>[a-z\_]+)/indicators/?$',
        'snisi_web.views.mapping.get_indicator_data',
        name='domain_indicator'),

    url(r'^api/indicators/geo/?$',
        'snisi_web.views.indicators_api.geojson_indicator',
        name='geojson_indicator'),

    # Indicators API
    url(r'^api/indicators/(?P<key>[a-zA-Z0-9\_]*)/?$',
        'snisi_web.views.indicators_api.list_all_indicators',
        name='api_indicators'),

    url(r'download-report/{receipt}.xls'.format(receipt=RGXP_RECEIPT),
        'snisi_web.views.raw_data.download_as_excel',
        name='download_report_xls'),

    url(r'map/?$',
        'snisi_web.views.mapping.webmap',
        {'template_name': 'map.html'},
        name='map'),

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
