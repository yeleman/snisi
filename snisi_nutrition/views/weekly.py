#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim: ai ts=4 sts=4 et sw=4 nu

from __future__ import (unicode_literals, absolute_import,
                        division, print_function)
import logging
import datetime

from django.shortcuts import render
from django.contrib.auth.decorators import login_required

from snisi_core.models.Projects import Cluster
from snisi_core.models.Periods import MonthPeriod
from snisi_core.models.Entities import Entity
from snisi_nutrition.models.Weekly import (
    WeeklyNutritionR, AggWeeklyNutritionR, NutWeekPeriod)
from snisi_web.utils import entity_periods_context
from snisi_nutrition import (ROUTINE_EXTENDED_REPORTING_END_DAYS_DELTA,
                             ROUTINE_DISTRICT_AGG_DAYS_DELTA,
                             ROUTINE_REGION_AGG_DAYS_DELTA)

logger = logging.getLogger(__name__)


def important_weekly_day_names():
    p = NutWeekPeriod.current()
    end_ext = p.end_on + datetime.timedelta(
        days=ROUTINE_EXTENDED_REPORTING_END_DAYS_DELTA)
    agg_ds = p.end_on + datetime.timedelta(
        days=ROUTINE_DISTRICT_AGG_DAYS_DELTA, seconds=100)
    agg_rs = p.end_on + datetime.timedelta(
        days=ROUTINE_REGION_AGG_DAYS_DELTA, seconds=100)
    return (end_ext.strftime('%A').lower(),
            agg_ds.strftime('%A').lower(),
            agg_rs.strftime('%A').lower())


def nutperiods_for(month_periods):
    if not isinstance(month_periods, (list, tuple)):
        month_periods = [month_periods]
    periods = []
    for month_period in month_periods:
        for day in (1, 7, 14, 21, 28, 30, 21):
            dd = month_period.start_on + datetime.timedelta(days=day)
            try:
                p = NutWeekPeriod.find_create_by_date(dd)
            except:
                continue
            if p not in periods:
                periods.append(p)
    return periods


@login_required
def display_weekly(request,
                   entity_slug=None,
                   perioda_str=None,
                   periodb_str=None,
                   **kwargs):
    context = {}

    root = request.user.location
    cluster = Cluster.get_or_none('nutrition_routine')

    entity = Entity.get_or_none(entity_slug) or root

    # report_cls depends on entity
    try:
        report_cls = WeeklyNutritionR \
            if entity.type.slug == 'health_center' else AggWeeklyNutritionR
    except:
        report_cls = None

    context.update(entity_periods_context(
        request=request,
        root=root,
        cluster=cluster,
        view_name='nutrition_weekly',
        entity_slug=entity_slug,
        report_cls=report_cls,
        perioda_str=perioda_str,
        periodb_str=periodb_str,
        period_cls=MonthPeriod,
        assume_previous=False,
        must_be_in_cluster=True,
        backlog_periods=2,
    ))

    extended_end, district_agg, region_agg = important_weekly_day_names()
    context.update({
        'day_ext_end': extended_end,
        'day_agg_ds': district_agg,
        'day_agg_rs': region_agg
    })

    if report_cls:
        weekly_data = []
        for week_period in nutperiods_for(context['periods']):
            d = {'week_period': week_period}
            try:
                report = report_cls.objects.get(
                    entity=entity, period=week_period)
            except report_cls.DoesNotExist:
                report = None
            d.update({'report': report})
            weekly_data.append(d)

        context.update({'weekly_data': weekly_data})

    return render(request,
                  kwargs.get('template_name', 'nutrition/weekly.html'),
                  context)
