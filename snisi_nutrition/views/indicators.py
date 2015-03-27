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
from django.http import HttpResponse

from snisi_core.models.Entities import Entity
from snisi_core.models.Periods import MonthPeriod
from snisi_core.models.Projects import Cluster
from snisi_core.models.Reporting import ExpectedReporting
from snisi_core.permissions import provider_allowed_or_denied, user_root_for
from snisi_web.utils import (
    entity_periods_context, periods_from_url,
    ensure_entity_in_cluster, ensure_entity_at_least)
from snisi_web.decorators import user_role_within
from snisi_nutrition import period_is_complete
from snisi_nutrition.models.Monthly import NutritionR, AggNutritionR
from snisi_nutrition.indicators.common import RSCompletionTable
from snisi_nutrition.indicators.mam import (
    URENAMNewCasesTable, MAMNewCasesTable,
    MAMPerformanceTable, MAMPerformanceGraph,
    RSMAMCaseloadTable, RSMAMPerformance, MAMNewCasesGraph,
    MAMCaseloadTreatedGraph, MAMNewCasesByDS, MAMPerformanceByDS,
    MAMCaseloadTreatedByDS, MAMPerformanceByHC)
from snisi_nutrition.indicators.sam import (
    URENIURENASNewCasesTable, SAMNewCasesTable, SAMCaseloadTable,
    URENIURENASRepartitionTableURENIOnly,
    URENIURENASRepartitionTable, SAMPerformanceTable,
    URENIURENASRepartitionGraph, SAMPerformanceGraph,
    URENIURENASNewCasesTableWithEntities, URENASNewCasesByHC,
    RSSAMCaseloadTable, RSSAMRepartition,
    RSURENIPerformance, RSURENASPerformance,
    SAMNewCasesGraph, SAMCaseloadTreatedGraph,
    SAMNewCasesByDS, SAMRepartitionByDS, SAMPerformanceByDS,
    SAMCaseloadTreatedByDS, SAMPerformanceByHC)
from snisi_nutrition.utils import (
    generate_sum_data_table_for, generate_entities_periods_matrix)
from snisi_nutrition.xls_export import nutrition_overview_xls

logger = logging.getLogger(__name__)


@login_required
@user_role_within(['charge_sis', 'dtc'])
def dashboard(request, **kwargs):

    now = timezone.now()
    last_period = MonthPeriod.current().previous() if now.day < 26 else None
    periods = MonthPeriod.all_from(
        MonthPeriod.from_url_str("11-2014"), last_period)
    entity = request.user.location.casted()

    context = {
        'periods': periods,
        'entity': entity,
    }

    if entity.has_ureni or entity.has_urenas:
        context.update({
            'sam_performance': SAMPerformanceTable(entity=entity,
                                                   periods=periods)
        })
    if entity.has_urenam:
        context.update({
            'mam_performance': MAMPerformanceTable(entity=entity,
                                                   periods=periods)
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

    cluster = Cluster.get_or_none('nutrition_routine')
    perm_slug = "access_{}".format(cluster.domain.slug)
    root = user_root_for(request.user, perm_slug)
    entity = Entity.get_or_none(entity_slug) or root

    # make sure requested entity is in cluster
    ensure_entity_in_cluster(cluster, entity)

    # check permissions on this entity and raise 403
    provider_allowed_or_denied(request.user, 'access_nutrition', entity)

    # mission browser is reserved to district-level and above
    ensure_entity_at_least(entity, 'health_district')

    # report_cls depends on entity
    report_classes = cluster.domain \
        .import_from('expected.report_classes_for')(cluster)
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
        if period_is_complete(period, entity)
    ]
    context.update({'periods_expecteds': periods_expecteds})

    total_table = generate_sum_data_table_for(entity=context['entity'],
                                              periods=context['periods'])
    uren = 'mam' if is_mam else 'sam'
    context.update({
        'total_table': total_table,
        'overview_xls_slug': 'nutrition_overview_{u}_xls'.format(u=uren)})

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
def overview_generic_xls(request, entity_slug=None,
                         perioda_str=None, periodb_str=None,
                         is_sam=False, is_mam=False, **kwargs):

    cluster = Cluster.get_or_none('nutrition_routine')
    perm_slug = "access_{}".format(cluster.domain.slug)
    root = user_root_for(request.user, perm_slug)
    entity = Entity.get_or_none(entity_slug) or root

    # make sure requested entity is in cluster
    ensure_entity_in_cluster(cluster, entity)

    # check permissions on this entity and raise 403
    provider_allowed_or_denied(request.user, 'access_nutrition', entity)

    # mission browser is reserved to district-level and above
    ensure_entity_at_least(entity, 'health_district')

    try:
        report_cls = NutritionR \
            if entity.type.slug == 'health_center' else AggNutritionR
    except:
        report_cls = None
    periods, all_periods, perioda, periodb = periods_from_url(
        perioda_str, periodb_str,
        report_cls=report_cls,
        period_cls=MonthPeriod,
        assume_previous=True)

    file_name, file_content = nutrition_overview_xls(
        entity, periods, is_sam=is_sam, is_mam=is_mam)
    file_content = file_content.getvalue()

    response = HttpResponse(file_content,
                            content_type='application/vnd.ms-excel')
    response['Content-Disposition'] = 'attachment; filename="{}"' \
        .format(file_name)
    response['Content-Length'] = len(file_content)

    return response


@login_required
def overview_mam_xls(request, entity_slug=None,
                     perioda_str=None, periodb_str=None, **kwargs):
    return overview_generic_xls(request,
                                entity_slug=entity_slug,
                                perioda_str=perioda_str,
                                periodb_str=periodb_str,
                                is_sam=False,
                                is_mam=True,
                                **kwargs)


@login_required
def overview_sam_xls(request, entity_slug=None,
                     perioda_str=None, periodb_str=None, **kwargs):
    return overview_generic_xls(request,
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

    cluster = Cluster.get_or_none('nutrition_routine')
    perm_slug = "access_{}".format(cluster.domain.slug)
    root = user_root_for(request.user, perm_slug)
    entity = Entity.get_or_none(entity_slug) or root

    # make sure requested entity is in cluster
    ensure_entity_in_cluster(cluster, entity)

    # check permissions on this entity and raise 403
    provider_allowed_or_denied(request.user, 'access_nutrition', entity)

    # mission browser is reserved to district-level and above
    ensure_entity_at_least(entity, 'health_district')

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
        allow_coming_year=True,
        full_lineage=['country', 'health_region', 'health_district'],
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

    cluster = Cluster.get_or_none('nutrition_routine')
    perm_slug = "access_{}".format(cluster.domain.slug)
    root = user_root_for(request.user, perm_slug)
    entity = Entity.get_or_none(entity_slug) or root

    # make sure requested entity is in cluster
    ensure_entity_in_cluster(cluster, entity)

    # check permissions on this entity and raise 403
    provider_allowed_or_denied(request.user, 'access_nutrition', entity)

    # mission browser is reserved to district-level and above
    ensure_entity_at_least(entity, 'health_district')

    indic_list = []
    if entity is not None:
        if entity.type.slug == 'health_district':
            if kwargs.get('is_sam', False):
                indic_list += [
                    ('sam_new_cases', URENIURENASNewCasesTable),
                    ('sam_caseload', SAMCaseloadTable),
                    ('sam_repartition', URENIURENASRepartitionTableURENIOnly),
                    ('sam_performance', SAMPerformanceTable),
                    ('sam_repartition_graph', URENIURENASRepartitionGraph),
                    ('sam_new_cases_hc_graph', URENASNewCasesByHC),
                    ('sam_performance_graph', SAMPerformanceGraph),
                    ('sam_caseload_treated_graph', SAMCaseloadTreatedGraph),
                    ('sam_performance_hc_graph', SAMPerformanceByHC),
                ]
            if kwargs.get('is_mam', False):
                indic_list += [
                    ('mam_new_cases', URENAMNewCasesTable),
                    ('mam_performance', MAMPerformanceTable),
                    ('mam_performance_graph', MAMPerformanceGraph),
                    ('mam_performance_hc_graph', MAMPerformanceByHC),
                ]

        elif entity.type.slug == 'health_region':
            if kwargs.get('is_sam', False):
                indic_list += [
                    ('sam_all_new_cases', SAMNewCasesTable),
                    ('sam_new_cases', URENIURENASNewCasesTable),
                    ('rs_completion', RSCompletionTable),
                    ('rs_sam_caseload', RSSAMCaseloadTable),
                    ('rs_sam_reparition', RSSAMRepartition),

                    ('rs_ureni_performance', RSURENIPerformance),
                    ('rs_urenas_performance', RSURENASPerformance),

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
