#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim: ai ts=4 sts=4 et sw=4 nu

from __future__ import (unicode_literals, absolute_import,
                        division, print_function)

from django.contrib.auth.decorators import login_required
from django.shortcuts import render


graph_json = None


@login_required
def user_dashboard(request):
    context = {'page_slug': 'dashboard'}

    # from snisi_core.models.Reporting import ExpectedReporting
    # from snisi_core.models.Periods import MonthPeriod
    # from snisi_malaria.models import MalariaR

    # global graph_json
    # if graph_json is None:

    #     all_periods = list(set([e.period.id for e in ExpectedReporting.objects.all()]))
    #     all_periods = MonthPeriod.objects.filter(id__in=all_periods).order_by('start_on')
    #     print(all_periods)

    #     def pc(exp, arrived):
    #         try:
    #             return arrived * 100 / exp
    #         except ZeroDivisionError:
    #             return 0

    #     graph_json = []
    #     for period in all_periods:
    #         pd = {'period': period,
    #               'nb_exp': ExpectedReporting.objects.filter(period=period).count(),
    #               'nb_arrived': MalariaR.objects.filter(period=period).count()}
    #         pd.update({'percent_arrived': pc(pd['nb_exp'], pd['nb_arrived'])})
    #         graph_json.append(pd)

    # context.update({
    #     'nb_expected_total': ExpectedReporting.objects.count(),
    #     'nb_arrived_total': 5,
    #     'graph_data': graph_json,
    # })

    return render(request, 'user_dashboard.html', context)
