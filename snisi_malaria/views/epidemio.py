#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim: ai ts=4 sts=4 et sw=4 nu

from __future__ import (unicode_literals, absolute_import,
                        division, print_function)
import logging

from django.http import Http404
from django.shortcuts import render
from django.core.exceptions import PermissionDenied
from django.contrib.auth.decorators import login_required

from snisi_core.models.Projects import Cluster
from snisi_core.models.Periods import MonthPeriod, Period
from snisi_core.models.FixedWeekPeriods import (FixedMonthFirstWeek,
                                                FixedMonthSecondWeek,
                                                FixedMonthThirdWeek,
                                                FixedMonthFourthWeek,
                                                FixedMonthFifthWeek)
from snisi_core.models.Entities import Entity
from snisi_tools.auth import can_view_entity
from snisi_malaria.models import AggEpidemioMalariaR
from snisi_web.utils import entity_browser_context, get_base_url_for_periods
from snisi_malaria.epidemio_utils import get_threshold

logger = logging.getLogger(__name__)


@login_required
def display_epidemio(request,
                     entity_slug=None,
                     perioda_str=None,
                     periodb_str=None,
                     **kwargs):
    context = {}

    root = request.user.location
    cluster = Cluster.get_or_none('malaria_weekly_epidemiology')

    entity = Entity.get_or_none(entity_slug)

    if entity is None:
        entity = root

    if entity is None:
        raise Http404("Aucune entité pour le code {}".format(entity_slug))

    # if not entity in cluster.members():
    #     entity = cluster.members()[-1]

    # check permissions on this entity and raise 403
    if not can_view_entity(request.user, entity):
        raise PermissionDenied

    def period_from_strid(period_str, reportcls=None):
        period = None
        if period_str:
            try:
                period = Period.from_url_str(period_str).casted()
            except:
                pass
        return period
    perioda = period_from_strid(perioda_str)
    periodb = period_from_strid(periodb_str)
    if periodb is None:
        periodb = MonthPeriod.current()
    if perioda is None:
        perioda = MonthPeriod.find_create_from(year=periodb.middle().year - 1,
                                               month=periodb.middle().month)

    if perioda is None or periodb is None:
        raise Http404("Période incorrecte.")

    if perioda > periodb:
        t = perioda
        perioda = periodb
        periodb = t
        del(t)

    try:
        first_period = MonthPeriod.find_create_by_date(
            AggEpidemioMalariaR.objects.all()
                               .order_by('period__start_on')[0].period.middle())
    except IndexError:
        first_period = MonthPeriod.current()
    all_periods = MonthPeriod.all_from(first_period)
    periods = MonthPeriod.all_from(perioda, periodb)

    context.update({
        'all_periods': [(p.strid(), p) for p in reversed(all_periods)],
        'perioda': perioda,
        'periodb': periodb,
        'periods': periods,
        'cluster': cluster,
        'base_url': get_base_url_for_periods(view_name='malaria_epidemio', entity=entity,
                                             perioda_str=perioda_str or perioda.strid(),
                                             periodb_str=periodb_str or periodb.strid())
    })

    context.update(entity_browser_context(
        root=root, selected_entity=entity,
        full_lineage=['country', 'health_region',
                      'health_district', 'health_center'],
        cluster=cluster))


    period_classes = [
        FixedMonthFirstWeek,
        FixedMonthSecondWeek,
        FixedMonthThirdWeek,
        FixedMonthFourthWeek,
        FixedMonthFifthWeek,
    ]

    # main data holder is a list (periods indexed) of dict
    # each containing the period, the threshold and for each fixed-week
    # the corresponding report if exist.
    epidemio_data = []
    for month_period in periods:

        month_data = {
            'period': month_period,
            'threshold': get_threshold(entity,
                                       month_period.middle().year,
                                       month_period.middle().month)}

        # loop on fixed weeks and try to find a period and report
        for periodcls in period_classes:
            week_period = periodcls.find_create_from(month_period.middle().year, month_period.middle().month)

            if week_period is not None:
                # retrieve weekly report
                try:
                    report = AggEpidemioMalariaR.objects.get(entity=entity, period=week_period)
                except AggEpidemioMalariaR.DoesNotExist:
                    continue

                # update data-dict
                month_data.update({'week{}'.format(week_period.FIXED_WEEK_NUM): report})
        epidemio_data.append(month_data)

    context.update({'epidemio_data': epidemio_data})

    return render(request,
                  kwargs.get('template_name', 'malaria/epidemio.html'),
                  context)
