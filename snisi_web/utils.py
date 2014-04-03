#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim: ai ts=4 sts=4 et sw=4 nu

from __future__ import (unicode_literals, absolute_import,
                        division, print_function)
import logging

from django.core.urlresolvers import reverse

from snisi_core.models.Entities import Entity
from snisi_tools.caching import json_cache_from_cluster

logger = logging.getLogger(__name__)


def get_slug_path_from(entity, lineage):
    ''' walk up the lineage to fetch Entity slugs

        Ex: {'health_center': "S5C4",
             'health_district: "8R92",
             'health_region': "2732"} '''

    slugs = {}
    if entity is None:
        return slugs

    rlineage = list(reversed(lineage))
    for idx, ts in enumerate(rlineage):
        if not len(slugs) and ts != entity.type.slug:
            continue
        if ts == entity.type.slug:
            slugs.update({ts: entity.slug})
            continue

        parent = getattr(
            Entity.get_or_none(slugs.get(rlineage[idx -1])),
            'get_{}'.format(ts), lambda: None)()
        if parent:
            slugs.update({ts: parent.slug})
    return slugs


def entity_browser_context(root,
                           full_lineage, selected_entity=None,
                           root_children=None, cluster=None):
    ''' prepare context data to feed the EntityFilterBrowser.js with '''

    if cluster is not None and root_children is None:
        root_children = json_cache_from_cluster(cluster).get(root.slug)

    # a dict of type_slug: entity_slug for all ascendants from selected
    selected_data = get_slug_path_from(selected_entity, full_lineage)
    # new lineage (list of type_slug) from root
    lineage = full_lineage[full_lineage.index(root.type.slug) + 1:]
    return {
        'root': root,
        'full_lineage': full_lineage,
        'lineage': lineage,
        'entity': selected_entity,
        'lineage_data': [selected_data.get(ts) for ts in lineage],
        # children of the first element
        'children': root_children if root_children else
                    getattr(root, 'get_{}s'.format(lineage[0]), lambda: [])(),
    }


def get_base_url_for_periods(view_name, entity,
                   perioda_str=None,
                   periodb_str=None):
    kwargs = {
       'entity_slug': entity.slug if entity is not None else None,
       'perioda_str': perioda_str,
       'periodb_str': periodb_str
    }
    for k, v in kwargs.items():
        if v is None:
            del(kwargs[k])
    return reverse(view_name, kwargs=kwargs)


def get_base_url_for_period(view_name, entity, period_str=None):
    kwargs = {
       'entity_slug': entity.slug if entity is not None else None,
       'period_str': period_str,
    }
    for k, v in kwargs.items():
        if v is None:
            del(kwargs[k])
    return reverse(view_name, kwargs=kwargs)
