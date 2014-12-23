#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim: ai ts=4 sts=4 et sw=4 nu

from __future__ import (unicode_literals, absolute_import,
                        division, print_function)

from django.shortcuts import render
from django.contrib.auth.decorators import login_required

from snisi_core.models.Periods import MonthPeriod
from snisi_core.models.Reporting import ExpectedReporting

from snisi_nutrition.indicators import get_geo_indicators


@login_required
def nutrition_map(request, template_name='nutrition/map.html'):

    context = {'page_slug': 'map'}

    periods = [MonthPeriod.objects.get(identifier=p['period'])
               for p
               in ExpectedReporting.objects.filter(
        report_class__slug='nutrition_monthly_routine')
        .order_by('period').values('period').distinct()]

    years = []
    months = {}
    for period in periods:
        if period.start_on.year not in years:
            years.append(period.start_on.year)
        if period.start_on.month not in months.keys():
            months.update({period.start_on.month:
                           period.start_on.strftime("%B")})

    context.update({'years': sorted(years),
                    'months': months,
                    'indicators': get_geo_indicators(),
                    'default_year': periods[-1].middle().year,
                    'default_month': periods[-1].middle().month})

    return render(request, template_name, context)
