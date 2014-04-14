#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim: ai ts=4 sts=4 et sw=4 nu

from __future__ import (unicode_literals, absolute_import,
                        division, print_function)
import logging
import json
import os

from snisi_core.models.Entities import Entity

logger = logging.getLogger(__name__)


def get_json_cache_fname(cluster):
    return os.path.join(cluster.domain.module_path,
                        'cache',
                        '{}_members.json'.format(cluster.slug))


def generate_json_cache_from_cluster_members(cluster, skip_slugs=[]):

    def _list_of_children(slug, list_of_allowed):
        return [e.casted().to_dict()
                for e in Entity.get_or_none(slug)
                               .get_natural_children(skip_slugs=skip_slugs)
                if e.slug in list_of_allowed]

    all_entities = []
    # get list of members
    # for each member, get list of ancestors
    for member in cluster.members():
        for ancestor in member.get_ancestors():
            if ancestor.type.slug in skip_slugs:
                continue
            all_entities.append(ancestor.slug)
        all_entities.append(member.slug)

    all_entities = list(set(all_entities))

    # merge the two into a unique list of entities
    # for each elem in that list, generate a list of n+1 children
    entities_children = {slug: _list_of_children(slug, all_entities)
                         for slug in all_entities}
    # dump that dict into JSON

    fname = get_json_cache_fname(cluster)
    with open(fname, 'w') as f:
        json.dump(entities_children, f, indent=4)

    return


def json_cache_from_cluster(cluster):
    cache = {}
    fname = get_json_cache_fname(cluster)
    try:
        with open(fname, 'r') as f:
            cache = json.load(f)
    except:
        pass

    return cache


def descendants_slugs(cluster, slug):
    descendants = []
    cache = json_cache_from_cluster(cluster)

    def _add_children(aslug, dest):
        for c in cache.get(aslug):
            dest.append(c['slug'])
            _add_children(c['slug'], dest)

    _add_children(slug, descendants)

    return list(set(descendants))


