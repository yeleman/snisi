#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim: ai ts=4 sts=4 et sw=4 nu

from __future__ import (unicode_literals, absolute_import,
                        division, print_function)
import logging

from django.shortcuts import render
from django.contrib.auth.decorators import login_required

from snisi_core.models.Projects import Cluster
from snisi_core.models.Periods import MonthPeriod
from snisi_core.models.FixedWeekPeriods import (FixedMonthFirstWeek,
                                                FixedMonthSecondWeek,
                                                FixedMonthThirdWeek,
                                                FixedMonthFourthWeek,
                                                FixedMonthFifthWeek)
from snisi_malaria.models import AggEpidemioMalariaR
from snisi_web.utils import entity_periods_context
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

    context.update(entity_periods_context(
        request=request,
        root=root,
        cluster=cluster,
        view_name='malaria_epidemio',
        entity_slug=entity_slug,
        report_cls=AggEpidemioMalariaR,
        perioda_str=perioda_str,
        periodb_str=periodb_str,
        period_cls=MonthPeriod,
        must_be_in_cluster=False,
        assume_previous=False,
    ))

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
    for month_period in context['periods']:

        month_data = {
            'period': month_period,
            'threshold': get_threshold(context['entity'],
                                       month_period.middle().year,
                                       month_period.middle().month)}

        # loop on fixed weeks and try to find a period and report
        for periodcls in period_classes:
            week_period = periodcls.find_create_from(
                month_period.middle().year, month_period.middle().month)

            if week_period is not None:
                # retrieve weekly report
                try:
                    report = AggEpidemioMalariaR.objects.get(
                        entity=context['entity'], period=week_period)
                except AggEpidemioMalariaR.DoesNotExist:
                    continue

                # update data-dict
                month_data.update({'week{}'.format(
                    week_period.FIXED_WEEK_NUM): report})
        epidemio_data.append(month_data)

    context.update({'epidemio_data': epidemio_data})

    return render(request,
                  kwargs.get('template_name', 'malaria/epidemio.html'),
                  context)
