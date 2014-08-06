#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim: ai ts=4 sts=4 et sw=4 nu

from __future__ import (unicode_literals, absolute_import,
                        division, print_function)
import json

from django.http import HttpResponse
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt

from snisi_core.models.Periods import MonthPeriod
from snisi_core.models.Projects import Domain
from snisi_core.models.Entities import HealthEntity
from snisi_malaria.indicators import get_indicators


def list_all_indicators(request, key=None):

    indicators = get_indicators(key)

    return HttpResponse(json.dumps(indicators),
                        content_type='application/json')


@require_POST
@csrf_exempt
def geojson_data(request, project_slug):

    domain = Domain.get_or_none(project_slug)

    get_geoindicators = domain.import_from('indicators.get_geoindicators')
    get_geoindicators()


@require_POST
@csrf_exempt
def geojson_indicator(request):

    feature_list = {
        "type": "FeatureCollection",
        "crs": {"type": "name",
                "properties": {
                    "name": "urn:ogc:def:crs:OGC:1.3:CRS84"}},
        "properties": {},
        "features": []
    }

    try:
        json_request = json.loads(request.body)
    except Exception as e:
        return HttpResponse(json.dumps({"error": e}))

    project_slug = json_request.get('project_slug')
    target_level = json_request.get('level')
    # display_hc = json_request.get('display_hc')
    indicator_slug = json_request.get('indicator_slug')
    timing = json_request.get('timing')  # single_period | evolution

    period_slug_a = json_request.get('period_a')
    period_a = MonthPeriod.from_url_str(period_slug_a)

    period_slug_b = json_request.get('period_b')
    if period_slug_b:
        period_b = MonthPeriod.from_url_str(period_slug_b)
    else:
        period_b = None

    domain = Domain.get_or_none(project_slug)
    indicator = domain.import_from('indicators.{}'.format(indicator_slug))

    for entity in HealthEntity.objects.filter(type__slug=target_level):

        if timing == 'single_period':
            indicator_instance = indicator(period=period_a, entity=entity)
            indicator_value_a = indicator_instance.data
            indicator_value_b = None

            indicator_value = indicator_value_a
        else:
            indicator_instance_a = indicator(period=period_a, entity=entity)
            indicator_instance_b = indicator(period=period_b, entity=entity)
            indicator_value_a = indicator_instance_a.data
            indicator_value_b = indicator_instance_b.data
            indicator_value = indicator_value_a - indicator_value_b

        entity_feature = {
            "type": "Feature",
            "properties": {
                "indicator_value_a": indicator_value_a,
                "indicator_value_b": indicator_value_b,
                "indicator_value": indicator_value,
                "indicator_value_human": indicator_instance.human(),
            }
        }
        entity_feature['properties'].update(entity.to_dict())

        if entity.geojson:
            entity_feature.update({"geometry": entity.geojson})

        feature_list['features'].append(entity_feature)

    indicator_values = list(set([v['properties']['indicator_value']
                                 for v in feature_list['features']]))
    try:
        indicator_values.remove(None)
    except:
        pass
    feature_list['properties'].update({
        "indicator_value_min": min(indicator_values),
        "indicator_value_max": max(indicator_values),
        "indicator_slug": indicator.spec()['slug'],
        "indicator_name": indicator.spec()['name']})

    return HttpResponse(json.dumps(feature_list),
                        content_type='application/json')
