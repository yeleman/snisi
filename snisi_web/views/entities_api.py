#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim: ai ts=4 sts=4 et sw=4 nu

from __future__ import (unicode_literals, absolute_import,
                        division, print_function)
import json

from django.http import HttpResponse, JsonResponse

from snisi_core.models.Entities import Entity
from snisi_core.models.Projects import Cluster
from snisi_tools.caching import json_cache_from_cluster


def get_detail(request, entity_slug=None):
    """ json results for passed entity """

    entity = Entity.get_or_none(entity_slug)
    if entity is None:
        data = None
    else:
        data = entity.to_dict()
    return JsonResponse(data)


def get_children(request, parent_slug=None, type_slug=None):
    """ json results of natural children for passed entity """

    return natural_children_as_json_view(request,
                                         parent_slug=parent_slug,
                                         type_slug=type_slug,
                                         skip_slugs=['health_area', 'vfq'],
                                         filter_func=None)


def get_cluster_children_live(request, cluster_slug,
                              parent_slug=None, type_slug=None):
    """ same get-children API but reduces results to members of cluster """

    cluster = Cluster.get_or_none(cluster_slug)
    if cluster is not None:
        filter_func = lambda e: e.casted() in cluster.members()

    return natural_children_as_json_view(request,
                                         parent_slug=parent_slug,
                                         type_slug=type_slug,
                                         skip_slugs=['health_area', 'vfq'],
                                         filter_func=filter_func)


def get_epidemio_children(request,
                          parent_slug=None, type_slug=None):
    """ same get-children API but reduces results to members of cluster """

    cluster = Cluster.get_or_none('malaria_weekly_epidemiology')

    def filter_func(e):
        if e.casted() in cluster.members():
            return True
        for m in cluster.members():
            if e.slug in [a.slug for a in m.get_ancestors()]:
                return True
        return False

    return natural_children_as_json_view(request,
                                         parent_slug=parent_slug,
                                         type_slug=type_slug,
                                         skip_slugs=['health_area', 'vfq'],
                                         filter_func=filter_func)


def get_cluster_children(request,
                         cluster_slug,
                         parent_slug=None,
                         type_slug=None,
                         skip_slugs=[]):

    if parent_slug == '___':
        parent_slug = 'mali'

    if type_slug == '__all__':
        type_slug = None

    cluster = Cluster.get_or_none(cluster_slug)
    if cluster is not None:
        children = json_cache_from_cluster(cluster).get(parent_slug)
    else:
        children = []

    return HttpResponse(json.dumps(children),
                        content_type='application/json')


def natural_children_as_json_view(request,
                                  parent_slug=None,
                                  type_slug=None,
                                  skip_slugs=[],
                                  filter_func=None):
    """ generic view to build json results of entities children list """

    # define the filter func based on provided parameter
    is_filter_compliant = lambda e: filter_func(e) if filter_func else True

    if parent_slug == '___':
        parent_slug = 'mali'

    if type_slug == '__all__':
        type_slug = None

    parent = Entity.get_or_none(parent_slug)
    if parent is None:
        children = []
    else:
        children = parent.get_natural_children(
            skip_slugs=['health_area', 'vfq'])

    return HttpResponse(json.dumps(
        [Entity.get_or_none(e.slug).to_dict()
         for e in children if is_filter_compliant(e)]),
        content_type='application/json')
