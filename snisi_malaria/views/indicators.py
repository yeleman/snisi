#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim: ai ts=4 sts=4 et sw=4 nu

from __future__ import (unicode_literals, absolute_import,
                        division, print_function)
import logging
import os

from django.shortcuts import render, redirect
from django.http import Http404
from django.contrib.auth.decorators import login_required
from django.conf import settings

from snisi_core.permissions import user_root_for, provider_allowed_or_denied
from snisi_core.models.Entities import Entity
from snisi_core.models.Periods import MonthPeriod, Period
from snisi_core.models.Reporting import ExpectedReporting
from snisi_core.models.Projects import Cluster
from snisi_web.utils import (
    entity_browser_context, get_base_url_for_periods, ensure_entity_in_cluster)
from snisi_tools.misc import import_path
from snisi_tools.path import mkdir_p
from snisi_malaria.rtf_export import generate_section_rtf
from snisi_malaria.models import MalariaR

logger = logging.getLogger(__name__)


@login_required
def browser(request,
            entity_slug=None,
            perioda_str=None,
            periodb_str=None,
            section_index='1', sub_section=None, **kwargs):

    context = {}
    cluster = Cluster.get_or_none('malaria_monthly_routine')
    perm_slug = "access_{}".format(cluster.domain.slug)
    root = user_root_for(request.user, perm_slug)
    entity = Entity.get_or_none(entity_slug) or root
    report_classes = cluster.domain.import_from(
        'expected.report_classes_for')(cluster)

    ensure_entity_in_cluster(cluster, entity)

    # check permissions on this entity and raise 403
    provider_allowed_or_denied(request.user, perm_slug, entity)

    def period_from_strid(period_str, reportcls=None):
        period = None
        if period_str:
            try:
                period = Period.from_url_str(period_str).casted()
            except:
                pass
        if not period and reportcls:
            period = reportcls.current()
        return period
    perioda = period_from_strid(perioda_str, MonthPeriod)
    periodb = period_from_strid(periodb_str, MonthPeriod)

    if perioda is None or periodb is None:
        raise Http404("Période incorrecte.")

    if perioda > periodb:
        t = perioda
        perioda = periodb
        periodb = t
        del(t)

    all_periods = sorted(list(set(
        [e.period.casted()
         for e in ExpectedReporting.objects.filter(entity=entity,
         report_class__in=report_classes)
         ])), key=lambda x: x.start_on)

    def get_periods(perioda, periodb):
        periods = []
        period = perioda
        while period <= periodb:
            periods.append(period)
            period = period.following()
        return periods
    periods = get_periods(perioda, periodb)

    context.update({
        'all_periods': [(p.strid(), p) for p in reversed(all_periods)],
        'perioda': perioda,
        'periodb': periodb,
        'periods': periods,
        'section_index': section_index,
        'section': "section{}".format(section_index),
        'sub_section': sub_section,
        'base_url': get_base_url_for_periods(
            view_name='malaria_view', entity=entity,
            perioda_str=perioda_str or perioda.strid(),
            periodb_str=periodb_str or periodb.strid())
    })

    context.update(entity_browser_context(
        root=root,
        selected_entity=entity,
        full_lineage=['country', 'health_region',
                      'health_district', 'health_center'],
        cluster=cluster))

    # get module from section/sub
    section_name = 'section{section_index}'.format(section_index=section_index)
    if sub_section:
        section_name += '_{sub_section}'.format(sub_section=sub_section)
    WIDGETS = import_path('snisi_malaria.indicators.{}.WIDGETS'
                          .format(section_name), failsafe=True)
    if WIDGETS is None:
        raise Http404("No section/sub_section for that request")

    section_title = import_path('snisi_malaria.indicators.{}.TITLE'
                                .format(section_name), failsafe=True)

    widgets = [w(periods=periods, entity=entity) for w in WIDGETS]

    context.update({'widgets': widgets, 'section_title': section_title})

    return render(request, kwargs.get('template_name',
                  'malaria/indicator_browser.html'), context)


@login_required
def export(request,
           entity_slug=None,
           perioda_str=None,
           periodb_str=None,
           section_index='1', sub_section=None, **kwargs):

    cluster = Cluster.get_or_none('malaria_monthly_routine')
    perm_slug = "access_{}".format(cluster.domain.slug)
    root = user_root_for(request.user, perm_slug)
    entity = Entity.get_or_none(entity_slug) or root
    ensure_entity_in_cluster(cluster, entity)
    provider_allowed_or_denied(request.user, perm_slug, entity)

    def period_from_strid(period_str, reportcls=None):
        period = None
        if period_str:
            try:
                period = Period.from_url_str(period_str).casted()
            except:
                pass
        if not period and reportcls:
            period = reportcls.current()
        return period
    perioda = period_from_strid(perioda_str, MonthPeriod)
    periodb = period_from_strid(periodb_str, MonthPeriod)

    if perioda is None or periodb is None:
        raise Http404("Période incorrecte.")

    if perioda > periodb:
        t = perioda
        perioda = periodb
        periodb = t
        del(t)

    def get_periods(perioda, periodb):
        periods = []
        period = perioda
        while period <= periodb:
            periods.append(period)
            period = period.following()
        return periods
    periods = get_periods(perioda, periodb)

    # get module from section/sub
    section_name = 'section{section_index}'.format(section_index=section_index)
    if sub_section:
        section_name += '_{sub_section}'.format(sub_section=sub_section)
    WIDGETS = import_path('snisi_malaria.indicators.{}.WIDGETS'
                          .format(section_name), failsafe=True)
    if WIDGETS is None:
        raise Http404("No section/sub_section for that request")
    section_title = import_path('snisi_malaria.indicators.{}.TITLE'
                                .format(section_name), failsafe=True)

    base_path = os.path.join("malaria", "sections", entity.slug)
    filename = "{entity}_{perioda}-{periodb}-{section}.rtf".format(
        entity=entity.slug,
        perioda=perioda.strid(),
        periodb=periodb.strid(),
        section=section_name)

    report_folder = os.path.join(settings.FILES_REPOSITORY, base_path)
    mkdir_p(report_folder)
    full_path = os.path.join(report_folder, filename)

    if not os.path.exists(full_path):
        generate_section_rtf(entity=entity,
                             periods=periods,
                             widget_dict=WIDGETS,
                             title=section_title,
                             base_path=base_path,
                             filename=filename)

    return redirect('protected', os.path.join(base_path, filename))


@login_required
def custom_indicator(request, **kwargs):

    context = {}

    cluster = Cluster.get_or_none('malaria_monthly_routine')

    speriod = ExpectedReporting.objects \
        .order_by('period__start_on').first().period
    all_periods = MonthPeriod.all_from(speriod)
    context.update({
        'all_periods': [(p.strid(), p) for p in reversed(all_periods)],
        'raw_indicators': MalariaR.data_fields,
        'entities': cluster.members(),
    })

    return render(request,
                  kwargs.get('template_name', 'malaria/custom_indicator.html'),
                  context)
