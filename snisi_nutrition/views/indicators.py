#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim: ai ts=4 sts=4 et sw=4 nu

from __future__ import (unicode_literals, absolute_import,
                        division, print_function)
import logging
import os

from django.shortcuts import render, redirect
from django.http import Http404
from django.core.exceptions import PermissionDenied
from django.contrib.auth.decorators import login_required
from django.conf import settings

from snisi_core.models.Entities import Entity
from snisi_core.models.Periods import MonthPeriod, Period
from snisi_core.models.Reporting import ExpectedReporting
from snisi_core.models.Projects import Cluster
from snisi_tools.auth import can_view_entity
from snisi_web.utils import entity_browser_context, get_base_url_for_periods
from snisi_tools.misc import import_path
from snisi_nutrition.models.Monthly import NutritionR

logger = logging.getLogger(__name__)


@login_required
def browser(request,
            entity_slug=None,
            perioda_str=None,
            periodb_str=None,
            section_index='1', sub_section=None, **kwargs):

    context = {}

    root = request.user.location

    cluster = Cluster.get_or_none('nutrition_routine')
    report_classes = cluster.domain.import_from(
        'expected.report_classes_for')(cluster)

    entity = Entity.get_or_none(entity_slug)
    if entity is None:
        entity = root

    if entity is None:
        raise Http404("Aucune entité pour le code {}".format(entity_slug))

    # check permissions on this entity and raise 403
    if not can_view_entity(request.user, entity):
        raise PermissionDenied

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

    # retrieve Indicator Table
    from snisi_nutrition.indicators import (PerformanceIndicators,
                                            FigurePerformanceIndicators,
                                            TableauPromptitudeRapportage,
                                            FigurePromptitudeRapportage)

    performance_table = PerformanceIndicators(entity=entity, periods=periods)
    performance_graph = FigurePerformanceIndicators(
        entity=entity, periods=periods)
    ontime_table = TableauPromptitudeRapportage(entity=entity, periods=periods)
    ontime_graph = FigurePromptitudeRapportage(entity=entity, periods=periods)

    context.update({
        'performance_table': performance_table,
        'performance_graph': performance_graph,
        'ontime_table': ontime_table,
        'ontime_graph': ontime_graph,
    })

    return render(request, kwargs.get('template_name',
                  'nutrition/indicators.html'), context)
