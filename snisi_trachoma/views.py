#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim: ai ts=4 sts=4 et sw=4 nu

from __future__ import (unicode_literals, absolute_import,
                        division, print_function)
import logging

from django.http import Http404
from django.shortcuts import render
from django.core.exceptions import PermissionDenied
from django.contrib.auth.decorators import login_required

from snisi_core.models.Projects import Cluster
from snisi_core.models.Periods import MonthPeriod, Period

from snisi_core.models.Entities import Entity
from snisi_tools.auth import can_view_entity
from snisi_trachoma.models import TTBacklogMissionR
from snisi_web.utils import (entity_browser_context, get_base_url_for_period,
                             get_base_url_for_periods)

logger = logging.getLogger(__name__)


@login_required
def trachoma_mission_browser(request,
                             entity_slug=None,
                             period_str=None,
                             **kwargs):
    context = {}

    root = request.user.location
    cluster = Cluster.get_or_none('trachoma_backlog')

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
        return period
    period = period_from_strid(period_str)
    if period is None:
        period = MonthPeriod.current()

    try:
        first_period = MonthPeriod.find_create_by_date(
            TTBacklogMissionR.objects.all()
            .order_by('period__start_on')[0].period.middle())
    except IndexError:
        first_period = MonthPeriod.current()
    all_periods = MonthPeriod.all_from(first_period)

    context.update({
        'all_periods': [(p.strid(), p) for p in reversed(all_periods)],
        'period': period,
        'base_url': get_base_url_for_period(
            view_name='trachoma_missions', entity=entity,
            period_str=period_str or period.strid())
    })

    context.update(entity_browser_context(
        root=root, selected_entity=entity,
        full_lineage=['country', 'health_region', 'health_district'],
        cluster=cluster))

    # retrieve list of missions for that period
    missions = TTBacklogMissionR.objects.filter(
        period=period,
        entity__slug__in=[e.slug for e in entity.get_health_districts()])

    context.update({'missions': missions})

    return render(request,
                  kwargs.get('template_name', 'trachoma/missions_list.html'),
                  context)


@login_required
def trachoma_mission_viewer(request, report_receipt, **kwargs):
    context = {}

    mission = TTBacklogMissionR.get_or_none(report_receipt)
    if mission is None:
        return Http404("Nº de reçu incorrect : {}".format(report_receipt))

    context.update({'mission': mission})

    return render(request,
                  kwargs.get('template_name', 'trachoma/mission_detail.html'),
                  context)


@login_required
def trachoma_dashboard(request,
                       entity_slug=None,
                       perioda_str=None,
                       periodb_str=None,
                       **kwargs):
    context = {}

    root = request.user.location
    cluster = Cluster.get_or_none('trachoma_backlog')

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
        return period
    perioda = period_from_strid(perioda_str)
    periodb = period_from_strid(periodb_str)
    if periodb is None:
        periodb = MonthPeriod.current()
    if perioda is None:
        perioda = periodb

    if perioda is None or periodb is None:
        raise Http404("Période incorrecte.")

    if perioda > periodb:
        t = perioda
        perioda = periodb
        periodb = t
        del(t)

    try:
        first_period = MonthPeriod.find_create_by_date(
            TTBacklogMissionR.objects.all().order_by(
                'period__start_on')[0].period.middle())
    except IndexError:
        first_period = MonthPeriod.current()
    all_periods = MonthPeriod.all_from(first_period)
    periods = MonthPeriod.all_from(perioda, periodb)

    context.update({
        'all_periods': [(p.strid(), p) for p in reversed(all_periods)],
        'periods': periods,
        'perioda': perioda,
        'periodb': periodb,
        'base_url': get_base_url_for_periods(
            view_name='trachoma_dashboard',
            entity=entity,
            perioda_str=perioda_str or perioda.strid(),
            periodb_str=periodb_str or periodb.strid())
    })

    context.update(entity_browser_context(
        root=root, selected_entity=entity,
        full_lineage=['country', 'health_region', 'health_district'],
        cluster=cluster))

    # retrieve Indicator Table
    from snisi_trachoma.indicators import (MissionDataSummary,
                                           CumulativeBacklogData)

    missions_followup = MissionDataSummary(entity=entity,
                                           periods=periods)
    cumulative_backlog = CumulativeBacklogData(entity=entity,
                                               periods=periods)

    context.update({
        'missions_followup': missions_followup,
        'cumulative_backlog': cumulative_backlog,
    })

    return render(request,
                  kwargs.get('template_name', 'trachoma/dashboard.html'),
                  context)
