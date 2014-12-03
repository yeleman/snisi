#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim: ai ts=4 sts=4 et sw=4 nu

from __future__ import (unicode_literals, absolute_import,
                        division, print_function)
import copy
import json

from django.http import HttpResponse
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from django.shortcuts import render

from snisi_core.models.Entities import Entity
from snisi_core.models.Projects import Domain
from snisi_core.models.Projects import Participation, Cluster
from snisi_core.models.Periods import MonthPeriod
from snisi_core.models.Reporting import ExpectedReporting
from snisi_web.views.tools import withCORS
from snisi_tools.misc import import_path


@login_required
def webmap(request, template_name='map.html'):
    context = {'page_slug': 'map'}

    # from snisi_malaria.indicators import get_geo_indicators

    periods = [MonthPeriod.objects.get(identifier=p['period'])
               for p
               in ExpectedReporting.objects
               .filter(period__period_type='month')
               .order_by('period').values('period').distinct()]

    indicators = {}
    for domain in Domain.active.all():
        geo_indic_func = domain.import_from('indicators.get_geo_indicators')
        if geo_indic_func is not None:
            # indicators[domain.slug] = geo_indic_func()
            for k, v in geo_indic_func().items():
                indicators.update({"{domain}#{section}"
                                   .format(domain=domain.name, section=k): v})

    years = []
    months = {}
    for period in periods:
        if period.start_on.year not in years:
            years.append(period.start_on.year)
        if period.start_on.month not in months.keys():
            months.update({period.start_on.month:
                           period.start_on.strftime("%B")})

    context.update({'years': sorted(years),
                    'months': months,
                    'indicators': indicators,
                    'default_year': periods[-1].middle().year,
                    'default_month': periods[-1].middle().month})

    return render(request, template_name, context)


def geojson_data(request, cluster_slug=None, parent_slug='mali'):

    mali = Entity.objects.get(slug='mali')
    cluster = Cluster.get_or_none(cluster_slug, True)

    featureColTemplate = {
        "type": "FeatureCollection",
        "crs": {"type": "name",
                "properties": {
                    "name": "urn:ogc:def:crs:OGC:1.3:CRS84"}},
        "properties": {},
        "features": []
    }

    def _getChildren(parent):
        qs = Participation.objects.filter(cluster=cluster)
        if parent.type.slug == 'health_district':
            qs = qs.filter(entity__parent__parent=parent)
        else:
            qs = qs.filter(entity__parent=parent)
        return [Entity.get_or_none(v['entity'])
                for v in qs.order_by('entity__name')
                .values('entity').distinct()]

    def _getChildCollection(parent):
        data = copy.deepcopy(featureColTemplate)
        data['properties'].update(parent.to_dict())
        if parent.type.slug == 'health_center':
            children_qs = []
        else:
            children_qs = _getChildren(parent)

        for child in children_qs:
            cgj = child.geojson_feature
            if child.type.slug not in ('health_center', 'vfq'):
                cgj['properties'].update({'children':
                                          _getChildCollection(parent=child)})
            data['features'].append(cgj)
        return data

    regions = {r.slug: _getChildCollection(Entity.get_or_none(r.slug))
               for r in _getChildren(mali)}

    return withCORS(HttpResponse(json.dumps(regions),
                    content_type='application/json'))


@require_POST
@csrf_exempt
def get_indicator_data(request, domain_slug='malaria'):

    try:
        json_request = json.loads(request.body)
    except Exception as e:
        return HttpResponse(json.dumps({"error": e}))

    domain = Domain.get_or_none(domain_slug)

    indicator_slug = json_request.get('indicator_slug')
    year = json_request.get('year')
    month = json_request.get('month')
    period = MonthPeriod.find_create_from(year=int(year), month=int(month))
    indicator = import_path('{}.indicators.{}'
                            .format(domain.module_path, indicator_slug))
    parent = Entity.get_or_none(json_request.get('entity_slug'))
    targets = parent.get_health_centers() \
        if parent.type.slug == 'health_district' \
        else parent.get_health_districts()
    computed_values = {}
    for entity in targets:
        ind = indicator(period=period, entity=entity)
        computed_values.update({entity.slug: {
            'slug': entity.slug,
            'data': ind.data,
            'hdata': ind.human,
            'is_not_expected': not ind.is_expected,
            'is_missing': ind.is_missing,
            'is_yesno': ind.is_yesno}})

    return withCORS(HttpResponse(json.dumps(computed_values),
                                 content_type='application/json'))
