#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim: ai ts=4 sts=4 et sw=4 nu

from __future__ import (unicode_literals, absolute_import,
                        division, print_function)
import logging

logger = logging.getLogger(__name__)

from snisi_tools.caching import generate_json_cache_from_cluster_members


def update_cluster_caches_for(cluster):
    return generate_json_cache_from_cluster_members(cluster,
        skip_slugs=['health_area', 'health_center', 'vfq'])
