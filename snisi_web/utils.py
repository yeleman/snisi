#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim: ai ts=4 sts=4 et sw=4 nu

from __future__ import (unicode_literals, absolute_import,
                        division, print_function)
import logging

from django.http import Http404
from django.core.urlresolvers import reverse
from django.core.exceptions import PermissionDenied

from snisi_core.permissions import user_root_for, provider_allowed_or_denied
from snisi_core.models.Entities import LEVELS
from snisi_core.models.Entities import Entity
from snisi_tools.caching import json_cache_from_cluster
from snisi_core.models.Periods import MonthPeriod, Period


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
            Entity.get_or_none(slugs.get(rlineage[idx - 1])),
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
    if root_children:
        children = root_children
    else:
        if not lineage:
            children = []
        else:
            children = getattr(
                root, 'get_{}s'.format(lineage[0]), lambda: [])(),
    return {
        'root': root,
        'full_lineage': full_lineage,
        'lineage': lineage,
        'entity': selected_entity,
        'lineage_data': [selected_data.get(ts) for ts in lineage],
        # children of the first element
        'children': children
    }


def get_base_url_for_periods(view_name, entity,
                             perioda_str=None,
                             periodb_str=None):
    kwargs = {'entity_slug': entity.slug if entity is not None else None,
              'perioda_str': perioda_str,
              'periodb_str': periodb_str}
    for k, v in kwargs.items():
        if v is None:
            del(kwargs[k])
    return reverse(view_name, kwargs=kwargs)


def get_base_url_for_period(view_name, entity, period_str=None):
    kwargs = {'entity_slug': entity.slug if entity is not None else None,
              'period_str': period_str}
    for k, v in kwargs.items():
        if v is None:
            del(kwargs[k])
    return reverse(view_name, kwargs=kwargs)


def periods_from_url(perioda_str, periodb_str,
                     period_cls, assume_previous, report_cls,
                     backlog_periods=12):

    def period_from_strid(period_str, report_cls=None):
        period = None
        base_cls = period_cls or Period
        if period_str:
            try:
                period = base_cls.from_url_str(period_str).casted()
            except:
                pass
        return period
    perioda = period_from_strid(perioda_str)
    periodb = period_from_strid(periodb_str)

    if periodb is None:
        periodb = period_cls.current()

    if perioda is None:
        perioda = periodb
        for __ in range(backlog_periods):
            perioda = perioda.previous()

    if perioda is None or periodb is None:
        raise Http404("Période incorrecte.")

    if perioda > periodb:
        t = perioda
        perioda = periodb
        periodb = t
        del(t)

    current_period = period_cls.current()

    if assume_previous:
        current_period = current_period.previous()

    first_period = current_period
    if report_cls is not None:
        try:
            first_period = period_cls.find_create_by_date(
                report_cls.objects.all().order_by('period__start_on')[0]
                                        .period.middle())
        except IndexError:
            pass

    all_periods = period_cls.all_from(first_period, current_period)
    periods = period_cls.all_from(perioda, periodb)

    return periods, all_periods, perioda, periodb


def entity_periods_context(request,
                           root,
                           cluster,
                           view_name,
                           entity_slug,
                           report_cls=None,
                           perioda_str=None,
                           periodb_str=None,
                           period_cls=MonthPeriod,
                           assume_previous=True,
                           must_be_in_cluster=False,
                           full_lineage=['country', 'health_region',
                                         'health_district', 'health_center'],
                           single_period=False,
                           backlog_periods=12):
    context = {}

    perm_slug = "access_{}".format(cluster.domain.slug)
    root = user_root_for(request.user, perm_slug)
    entity = Entity.get_or_none(entity_slug) or root

    if entity is None:
        raise Http404("Aucune entité pour le code {}".format(entity_slug))

    if must_be_in_cluster:
        ensure_entity_in_cluster(cluster, entity)

    # check permissions on this entity and raise 403
    provider_allowed_or_denied(request.user, perm_slug, entity)

    periods, all_periods, perioda, periodb = periods_from_url(
        perioda_str, periodb_str, period_cls=period_cls,
        assume_previous=assume_previous, report_cls=report_cls,
        backlog_periods=backlog_periods)

    if single_period:
        base_url = get_base_url_for_period(
            view_name=view_name, entity=entity, period_str=perioda_str)
    else:
        base_url = get_base_url_for_periods(
            view_name=view_name, entity=entity,
            perioda_str=perioda_str or perioda.strid(),
            periodb_str=periodb_str or periodb.strid())

    context.update({
        'all_periods': [(p.strid(), p) for p in reversed(all_periods)],
        'perioda': perioda,
        'periodb': periodb,
        'periods': periods,
        'cluster': cluster,
        'base_url': base_url,
        'view_name': view_name

    })

    context.update(entity_browser_context(
        root=root, selected_entity=entity,
        full_lineage=full_lineage,
        cluster=cluster))

    return context


def ensure_entity_in_cluster(cluster, entity):
    if not cluster.has_member(entity):
        raise PermissionDenied


def ensure_entity_at_least(entity, slug='health_district'):
    # not in entity.get_health_district().get_cancestors(include_self=True)
    if entity.level > LEVELS.get(slug):
        raise PermissionDenied
