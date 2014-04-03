#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim: ai ts=4 sts=4 et sw=4 nu

from __future__ import (unicode_literals, absolute_import,
                        division, print_function)
import json
import copy

from django.http import HttpResponse
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render
from django.contrib.auth.decorators import login_required

from snisi_core.models.Entities import Entity
from snisi_core.models.Projects import Participation, Cluster
from snisi_core.models.Periods import MonthPeriod
from snisi_core.models.Reporting import ExpectedReporting
from snisi_tools.misc import import_path

from snisi_malaria import get_domain
from snisi_malaria.indicators import get_geo_indicators

@login_required
def malaria_map(request, template_name='malaria/map.html'):

    context = {'page_slug': 'map'}

    periods = [MonthPeriod.objects.get(identifier=p['period'])
               for p in ExpectedReporting.objects \
                        .filter(report_class__slug='malaria_monthly_routine') \
                        .order_by('period').values('period').distinct()]

    years = []
    months = {}
    for period in periods:
        if not period.start_on.year in years:
            years.append(period.start_on.year)
        if not period.start_on.month in months.keys():
            months.update({period.start_on.month: period.start_on.strftime("%B")})

    context.update({'years': sorted(years),
                    'months': months,
                    'indicators': get_geo_indicators()})

    return render(request, template_name, context)


@require_POST
@csrf_exempt
def get_indicator_data(request):

    try:
        json_request = json.loads(request.body)
    except Exception as e:
        return HttpResponse(json.dumps({"error": e}))

    indicator_slug = json_request.get('indicator_slug')
    year = json_request.get('year')
    month = json_request.get('month')
    period = MonthPeriod.find_create_from(year=int(year), month=int(month))
    indicator = get_domain().import_from('indicators.{}'.format(indicator_slug))
    parent = Entity.get_or_none(json_request.get('entity_slug'))
    targets = parent.get_health_centers() if parent.type.slug == 'health_district' else parent.get_health_districts()
    computed_values = {}
    for entity in targets:
        ind = indicator(period=period, entity=entity)
        computed_values.update({entity.slug:
            {'slug': entity.slug,
             'data': ind.data,
             'hdata': ind.human,
             'is_not_expected': not ind.is_expected,
             'is_missing': ind.is_missing,
             'is_yesno': ind.is_yesno}})

    return HttpResponse(json.dumps(computed_values),
                        content_type='application/json')


def geojson_data(request, parent_slug='mali'):

    mali = Entity.objects.get(slug='mali')
    cluster = Cluster.get_or_none('malaria_monthly_routine')

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
                for v in qs.order_by('entity__name').values('entity').distinct()]

    def _getChildCollection(parent):
        data = copy.deepcopy(featureColTemplate)
        data['properties'].update(parent.to_dict())
        if parent.type.slug == 'health_center':
            children_qs =[]
        else:
            children_qs = _getChildren(parent)

        for child in children_qs:
            cgj = child.geojson_feature
            if not child.type.slug in ('health_center', 'vfq'):
                cgj['properties'].update({'children': _getChildCollection(parent=child)})
            data['features'].append(cgj)
        return data

    regions = {r.slug: _getChildCollection(Entity.get_or_none(r.slug))
               for r in _getChildren(mali)}

    return HttpResponse(json.dumps(regions),
                        content_type='application/json')
