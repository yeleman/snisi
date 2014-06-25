#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim: ai ts=4 sts=4 et sw=4 nu

from __future__ import (unicode_literals, absolute_import,
                        division, print_function)

from django.shortcuts import render

from snisi_core.models.Periods import MonthPeriod
from snisi_core.models.Reporting import ExpectedReporting
from snisi_vacc.indicators import get_geo_indicators

import logging

logger = logging.getLogger(__name__)


def vacc_map(request, **kwargs):
    context = {'page_slug': 'map'}

    periods = [MonthPeriod.objects.get(identifier=p['period'])
               for p in ExpectedReporting.objects \
                        .filter(report_class__slug='major_vaccine_monthly') \
                        .order_by('period').values('period').distinct()]

    years = []
    months = {}
    for period in periods:
        if not period.start_on.year in years:
            years.append(period.start_on.year)
        if not period.start_on.month in months.keys():
            months.update({period.start_on.month: period.start_on.strftime("%B")})

    context.update({'years': sorted(years),
                    'months': months,
                    'indicators': get_geo_indicators()})


    return render(request, kwargs.get('template_name',
                                      'vaccination/map.html'), context)
