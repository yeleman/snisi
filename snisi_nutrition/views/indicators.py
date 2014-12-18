#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim: ai ts=4 sts=4 et sw=4 nu

from __future__ import (unicode_literals, absolute_import,
                        division, print_function)
import logging
from collections import OrderedDict

from django.utils import timezone
from django.shortcuts import render
from django.contrib.auth.decorators import login_required

from snisi_core.models.Entities import Entity
from snisi_core.models.Periods import MonthPeriod
from snisi_core.models.Projects import Cluster
from snisi_core.models.Reporting import ExpectedReporting
from snisi_web.utils import entity_periods_context
from snisi_web.decorators import user_role_within
from snisi_nutrition.models.Monthly import NutritionR, AggNutritionR
from snisi_nutrition.indicators.common import (
    PromptnessReportingTable, PromptnessReportingFigure, RSCompletionTable)
from snisi_nutrition.indicators.mam import (
    URENAMNewCasesTable, MAMNewCasesTable,
    MAMCaseloadTreated, MAMPerformanceTable, MAMPerformanceGraph,
    RSMAMCaseloadTable, RSMAMPerformance, MAMNewCasesGraph,
    MAMCaseloadTreatedGraph, MAMNewCasesByDS, MAMPerformanceByDS,
    MAMCaseloadTreatedByDS)
from snisi_nutrition.indicators.sam import (
    URENIURENASNewCasesTable, SAMNewCasesTable, SAMCaseloadTable,
    URENIURENASRepartitionTable, SAMPerformanceTable,
    URENIURENASRepartitionGraph, SAMPerformanceGraph,
    URENIURENASNewCasesTableWithEntities, URENASNewCasesByHC,
    RSSAMCaseloadTable, RSSAMRepartition, RSSAMPerformance,
    SAMNewCasesGraph, SAMCaseloadTreatedGraph,
    SAMNewCasesByDS, SAMRepartitionByDS, SAMPerformanceByDS,
    SAMCaseloadTreatedByDS)
from snisi_nutrition.utils import (
    generate_sum_data_table_for, generate_entities_periods_matrix)

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

    promptness_table = PromptnessReportingTable(entity=entity,
                                                periods=periods)
    promptness_graph = PromptnessReportingFigure(entity=entity,
                                                 periods=periods)

    context.update({
        'promptness_table': promptness_table,
        'promptness_graph': promptness_graph,
    })

    return render(request, kwargs.get('template_name',
                  'nutrition/dashboard.html'), context)


@login_required
def overview_generic(request, entity_slug=None,
                     perioda_str=None, periodb_str=None,
                     is_sam=False, is_mam=False, **kwargs):
    context = {
        'is_sam': is_sam,
        'is_mam': is_mam
    }

    root = request.user.location
    cluster = Cluster.get_or_none('nutrition_routine')
    report_classes = cluster.domain \
        .import_from('expected.report_classes_for')(cluster)

    entity = Entity.get_or_none(entity_slug) or root

    # report_cls depends on entity
    try:
        report_cls = NutritionR \
            if entity.type.slug == 'health_center' else AggNutritionR
    except:
        report_cls = None

    view_name = 'nutrition_overview_sam' \
        if is_sam else 'nutrition_overview_mam'

    context.update(entity_periods_context(
        request=request,
        root=root,
        cluster=cluster,
        view_name=view_name,
        entity_slug=entity_slug,
        report_cls=report_cls,
        perioda_str=perioda_str,
        periodb_str=periodb_str,
        period_cls=MonthPeriod,
        must_be_in_cluster=True,
        full_lineage=['country', 'health_region', 'health_district'],
    ))

    # if entity.type.slug == 'health_district':
    periods_expecteds = [
        (period, ExpectedReporting.objects.filter(
            period=period, entity=context['entity'],
            report_class__in=report_classes).last())
        for period in context['periods']
    ]
    context.update({'periods_expecteds': periods_expecteds})

    total_table = generate_sum_data_table_for(entity=context['entity'],
                                              periods=context['periods'])
    context.update({'total_table': total_table})

    return render(request,
                  kwargs.get('template_name', 'nutrition/overview.html'),
                  context)


@login_required
def overview_mam(request, entity_slug=None,
                 perioda_str=None, periodb_str=None, **kwargs):
    return overview_generic(request,
                            entity_slug=entity_slug,
                            perioda_str=perioda_str,
                            periodb_str=periodb_str,
                            is_sam=False,
                            is_mam=True,
                            **kwargs)


@login_required
def overview_sam(request, entity_slug=None,
                 perioda_str=None, periodb_str=None, **kwargs):
    return overview_generic(request,
                            entity_slug=entity_slug,
                            perioda_str=perioda_str,
                            periodb_str=periodb_str,
                            is_sam=True,
                            is_mam=False,
                            **kwargs)


@login_required
def indicators_browser(request,
                       entity_slug=None,
                       perioda_str=None,
                       periodb_str=None,
                       indicators={},
                       context={},
                       view_name='indicators_browser',
                       **kwargs):

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
        view_name=view_name,
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

    entities_periods = generate_entities_periods_matrix(
        entity=context['entity'], periods=context['periods'])
    context.update({'entities_periods': entities_periods})

    return render(request,
                  kwargs.get('template_name', 'nutrition/indicators.html'),
                  context)


@login_required
def sam_synthesis_browser(request, entity_slug=None,
                          perioda_str=None, periodb_str=None, **kwargs):
    kwargs.update({'is_sam': True})
    return synthesis_browser(
        request=request, entity_slug=entity_slug,
        perioda_str=perioda_str, periodb_str=periodb_str,
        view_name='nutrition_synthesis_sam', **kwargs)


@login_required
def mam_synthesis_browser(request, entity_slug=None,
                          perioda_str=None, periodb_str=None, **kwargs):
    kwargs.update({'is_mam': True})
    return synthesis_browser(
        request=request, entity_slug=entity_slug,
        perioda_str=perioda_str, periodb_str=periodb_str,
        view_name='nutrition_synthesis_mam', **kwargs)


@login_required
def synthesis_browser(request,
                      entity_slug=None,
                      perioda_str=None,
                      periodb_str=None,
                      view_name='synthesis_browser',
                      **kwargs):
    context = {}

    if 'template_name' not in kwargs.keys():
        kwargs.update({'template_name': 'nutrition/synthesis.html'})

    entity = Entity.get_or_none(entity_slug)
    indic_list = []
    if entity is not None:
        if entity.type.slug == 'health_district':
            if kwargs.get('is_sam', False):
                indic_list += [
                    ('sam_new_cases', URENIURENASNewCasesTable),
                    ('sam_caseload', SAMCaseloadTable),
                    ('sam_repartition', URENIURENASRepartitionTable),
                    ('sam_performance', SAMPerformanceTable),
                    ('sam_repartition_graph', URENIURENASRepartitionGraph),
                    ('sam_new_cases_hc_graph', URENASNewCasesByHC),
                    ('sam_performance_graph', SAMPerformanceGraph),
                ]
            if kwargs.get('is_mam', False):
                indic_list += [
                    ('mam_new_cases', URENAMNewCasesTable),
                    ('mam_performance', MAMPerformanceTable),
                    ('mam_performance_graph', MAMPerformanceGraph),
                ]

        elif entity.type.slug == 'health_region':
            if kwargs.get('is_sam', False):
                indic_list += [
                    ('sam_new_cases', URENIURENASNewCasesTable),
                    ('sam_all_new_cases', SAMNewCasesTable),
                    ('rs_completion', RSCompletionTable),
                    ('rs_sam_caseload', RSSAMCaseloadTable),
                    ('rs_sam_reparition', RSSAMRepartition),
                    ('rs_sam_performance', RSSAMPerformance),
                    ('sam_new_cases_graph', SAMNewCasesGraph),
                    ('sam_repartition_graph', URENIURENASRepartitionGraph),
                    ('sam_performance_graph', SAMPerformanceGraph),
                    ('sam_caseload_treated_graph', SAMCaseloadTreatedGraph),
                    ('sam_new_cases_ds_graph', SAMNewCasesByDS),
                    ('sam_repartition_ds_graph', SAMRepartitionByDS),
                    ('sam_performance_ds_graph', SAMPerformanceByDS),
                    ('sam_caseload_treated_ds_graph', SAMCaseloadTreatedByDS),
                ]
            if kwargs.get('is_mam', False):
                indic_list += [
                    ('mam_new_cases', URENAMNewCasesTable),
                    ('rs_completion', RSCompletionTable),
                    ('rs_mam_caseload', RSMAMCaseloadTable),
                    ('rs_mam_performance', RSMAMPerformance),
                    ('mam_new_cases_graph', MAMNewCasesGraph),
                    ('mam_performance_graph', MAMPerformanceGraph),
                    ('mam_caseload_treated_graph', MAMCaseloadTreatedGraph),
                    ('mam_new_cases_ds_graph', MAMNewCasesByDS),
                    ('mam_performance_ds_graph', MAMPerformanceByDS),
                    ('mam_caseload_treated_ds_graph', MAMCaseloadTreatedByDS),
                ]

        elif entity.type.slug == 'health_center':
            pass
        elif entity.type.slug == 'country':
            pass

    indicators = OrderedDict(indic_list)

    return indicators_browser(request=request,
                              entity_slug=entity_slug,
                              perioda_str=perioda_str,
                              periodb_str=periodb_str,
                              indicators=indicators,
                              context=context,
                              view_name=view_name,
                              **kwargs)
