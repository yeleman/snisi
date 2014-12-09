#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim: ai ts=4 sts=4 et sw=4 nu

from __future__ import (unicode_literals, absolute_import,
                        division, print_function)
import logging
from collections import OrderedDict

from django.utils import timezone
from django.shortcuts import render
from django.http import Http404
from django.core.exceptions import PermissionDenied
from django.contrib.auth.decorators import login_required

from snisi_core.models.Entities import Entity
from snisi_core.models.Periods import MonthPeriod, Period
from snisi_core.models.Reporting import ExpectedReporting
from snisi_core.models.Projects import Cluster
from snisi_tools.auth import can_view_entity
from snisi_web.utils import entity_browser_context, get_base_url_for_periods
from snisi_web.utils import entity_periods_context
from snisi_web.decorators import user_role_within
from snisi_nutrition.models.Monthly import NutritionR, AggNutritionR
from snisi_nutrition.indicators import (TableNouvellesAdmissionsURENIURENAS,
                                        TableNouvellesAdmissionsURENAM,
                                        TableCaseloadSAM,
                                        TableRepartitionURENIURENAS,
                                        TablePerformanceSAM,
                                        TablePerformanceMAM,
                                        GraphRepartitionURENIURENAS,
                                        GraphNouvellesAdmissionsURENIURENAS,
                                        GraphPerformanceSAM,
                                        GraphPerformanceMAM)

logger = logging.getLogger(__name__)


@login_required
@user_role_within(['charge_sis', 'dtc'])
def dashboard(request, **kwargs):

    now = timezone.now()
    last_period = MonthPeriod.current().previous() if now.day < 26 else None
    periods = MonthPeriod.all_from(
        MonthPeriod.from_url_str("10-2014"), last_period)
    entity = request.user.location

    context = {
        'periods': periods,
        'entity': entity,
    }

    from snisi_nutrition.indicators import (PerformanceIndicators)

    performance_table = PerformanceIndicators(entity=entity, periods=periods)

    context.update({
        'performance_table': performance_table,
    })

    return render(request, kwargs.get('template_name',
                  'nutrition/dashboard.html'), context)


@login_required
def indicators_browser(request,
                       entity_slug=None,
                       perioda_str=None,
                       periodb_str=None,
                       indicators={},
                       **kwargs):
    context = {}

    root = request.user.location
    cluster = Cluster.get_or_none('nutrition_routine')

    entity = Entity.get_or_none(entity_slug) or root

    # report_cls depends on entity
    try:
        report_cls = NutritionR \
            if entity.type.slug == 'health_center' else AggNutritionR
    except:
        report_cls = None

    context.update(entity_periods_context(
        request=request,
        root=root,
        cluster=cluster,
        view_name='nutrition_weekly',
        entity_slug=entity_slug,
        report_cls=report_cls,
        perioda_str=perioda_str,
        periodb_str=periodb_str,
        period_cls=MonthPeriod,
        must_be_in_cluster=True,
    ))

    for indic_slug, indic_cls in indicators.items():
        indicators[indic_slug] = indic_cls(entity=entity,
                                           periods=context['periods'])
        context.update({indic_slug: indicators[indic_slug]})
    context.update({'indicators': indicators})

    return render(request,
                  kwargs.get('template_name', 'nutrition/indicators.html'),
                  context)


@login_required
def synthesis_browser(request,
                      entity_slug=None,
                      perioda_str=None,
                      periodb_str=None,
                      **kwargs):

    if 'template_name' not in kwargs.keys():
        kwargs.update({'template_name': 'nutrition/synthesis.html'})

    entity = Entity.get_or_none(entity_slug)
    if entity is not None:
        if entity.type.slug == 'health_district':
            indicators = OrderedDict([
                ('sam_new_cases', TableNouvellesAdmissionsURENIURENAS),
                ('mam_new_cases', TableNouvellesAdmissionsURENAM),
                ('sam_caseload', TableCaseloadSAM),
                ('sam_repartition', TableRepartitionURENIURENAS),
                ('sam_performance', TablePerformanceSAM),
                ('mam_performance', TablePerformanceMAM),
                ('sam_repartition_graph', GraphRepartitionURENIURENAS),
                # ('sam_new_cases_graph', GraphNouvellesAdmissionsURENIURENAS),
                ('sam_performance_graph', GraphPerformanceSAM),
                ('mam_performance_graph', GraphPerformanceMAM),
            ])
        elif entity.type.slug == 'health_region':
            indicators = OrderedDict([
            ])
        elif entity.type.slug == 'health_center':
            indicators = OrderedDict([
            ])
        elif entity.type.slug == 'country':
            indicators = OrderedDict([
            ])

    return indicators_browser(request=request,
                              entity_slug=entity_slug,
                              perioda_str=perioda_str,
                              periodb_str=periodb_str,
                              indicators=indicators,
                              **kwargs)
