#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim: ai ts=4 sts=4 et sw=4 nu

from __future__ import (unicode_literals, absolute_import,
                        division, print_function)
import logging

logger = logging.getLogger(__name__)

from snisi_tools.caching import generate_json_cache_from_cluster_members


def update_cluster_caches_for(cluster):
    # dispatch to a dedicated function per cluster
    return {
        'msi_reprohealth_routine': update_msi_monthly_routine_cache,
        'msi_reprohealth_routine_sms': update_msi_monthly_routine_sms_cache
    }.get(cluster.slug, lambda c: False)(cluster)


def update_msi_monthly_routine_cache(cluster):
    # update member's list JSON cache.
    return generate_json_cache_from_cluster_members(
        cluster, skip_slugs=['health_area', 'vfq'])


def update_msi_monthly_routine_sms_cache(cluster):
    # routine SMS needs no particular cache at the moment.
    # all routine SMS are part of monthly routine already
    return
