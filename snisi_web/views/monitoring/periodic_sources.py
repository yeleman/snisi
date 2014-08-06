#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim: ai ts=4 sts=4 et sw=4 nu

from __future__ import (unicode_literals, absolute_import,
                        division, print_function)

from django.contrib.auth.decorators import login_required
from django.shortcuts import render

from snisi_core.models.Entities import Entity
from snisi_core.models.Periods import MonthPeriod
from snisi_core.models.Reporting import ExpectedReporting, PERIODICAL_SOURCE
from snisi_web.decorators import user_role_within


@login_required
@user_role_within(['snisi_tech'])
def periodic_source_dashboard(request, **kwargs):
    context = {}

    if request.GET.get('entity'):
        entity = Entity.get_or_none(request.GET.get('entity'))
        context.update({'filter_entity': entity})
    else:
        entity = None

    period = MonthPeriod.current().previous()

    expected_reports = ExpectedReporting.objects.filter(
        report_class__report_type=PERIODICAL_SOURCE,
        within_period=False,
        within_entity=False,
        period=period,
        completion_status__in=('', ExpectedReporting.COMPLETION_MISSING),
        ).order_by('entity__parent__parent__parent__name',
                   'entity__parent__parent__name',
                   'entity__name')

    if entity:
        expected_reports = expected_reports.filter(entity=entity)

    context.update({'expected_reports': expected_reports})

    return render(request,
                  kwargs.get('template_name',
                             "monitoring/periodic_source.html"), context)
