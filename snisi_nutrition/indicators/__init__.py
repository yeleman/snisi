#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim: ai ts=4 sts=4 et sw=4 nu

from __future__ import (unicode_literals, absolute_import,
                        division, print_function)
import logging

from snisi_tools.misc import import_path

logger = logging.getLogger(__name__)
excludes = ['MalariaIndicator', 'Indicator']


def get_section(section_name):
    return import_path('{}.{}'.format(__name__, section_name))


def is_indicator(module, member, only_geo=False):
    ind = get_indicator(module, member)
    if not getattr(ind, 'SNISI_INDICATOR', None) or member in excludes:
        return False
    if only_geo and not getattr(ind, 'is_geo_friendly', None):
        return False
    return True


def get_indicator(module, member):
    return getattr(module, member)


def get_indicators(key=None, only_geo=False):
    sections = []
    umap = {'mam': "MAM", 'sam': "MAS"}

    for section_slug in range('mam', 'sam'):
        section_name = umap.get(section_slug)
        section = get_section(section_slug)

        section_data = {'slug': section_slug,
                        'name': section_name,
                        'indicators': [
                            get_indicator(section, indic_name).spec()
                            for indic_name in dir(section)
                            if is_indicator(section, indic_name, only_geo)]}
        if key == section_slug:
            return section_data
        sections.append(section_data)

    return [sec for sec in sections if len(sec['indicators'])]


def get_geo_indicators():
    indicators = {}
    section = get_section("map")
    section_path = "map"
    for indicator_name in dir(section):
        if not is_indicator(section, indicator_name, True):
            continue
        indicator = import_path('snisi_nutrition.indicators.map.{}'
                                .format(indicator_name))
        geo_section = getattr(indicator, 'geo_section', None)
        if geo_section not in indicators.keys():
            indicators.update({geo_section: []})
        spec = indicator.spec()
        spec.update({'slug': '{}.{}'.format(section_path,
                                            indicator.__name__)})
        indicators[geo_section].append(spec)

    return indicators
