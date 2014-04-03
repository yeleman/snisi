#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim: ai ts=4 sts=4 et sw=4 nu

from __future__ import (unicode_literals, absolute_import,
                        division, print_function)
import logging
import os

# from django.http import Http404
from django.conf import settings
from django.shortcuts import render
from django.contrib.auth.decorators import login_required

from snisi_core.models.Projects import Cluster
from snisi_core.models.Entities import Entity
from snisi_core.models.Periods import MonthPeriod
from snisi_tools.path import modified_on
from snisi_web.utils import entity_browser_context

logger = logging.getLogger(__name__)


@login_required
def display_report(request, entity_slug=None, **kwargs):

    context = {}


    def periods_for_quarter(year, quarter_num):
        start_period = MonthPeriod.find_create_from(
            year=int(year),
            month={'1': 1, '2': 4, '3': 7, '4': 10}.get(quarter_num),
            dont_create=True)
        periods = [start_period]
        for _ in range(1, 3):
            periods.append(periods[-1].following())
        return periods

    root = request.user.location
    entity = Entity.get_or_none(entity_slug)
    if entity is None:
        entity = root

    relative_folder = os.path.join("malaria", "quarter_reports")
    report_folder = os.path.join(settings.FILES_REPOSITORY, relative_folder)

    reports = []
    for fname in os.listdir(report_folder):
        if not fname.endswith('.rtf') and not fname.endswith('.doc'):
            continue

        try:
            fdata = fname.rsplit('.', 1)[0]
            slug = fdata.split('-', 1)[0]
            quarter = fdata.rsplit('_', 1)[1]
            qnum, year = quarter[1:].split('-')
        except:
            continue
        else:
            if entity.slug == slug:

                periods = periods_for_quarter(year, qnum)
                fpath = os.path.join(relative_folder, fname)
                fmodified_on = modified_on(os.path.join(report_folder, fname))
                reports.append({
                    'fname': fname,
                    'fpath': fpath,
                    'quarter': quarter,
                    'periods': periods,
                    'speriod': periods[0],
                    'eperiod': periods[-1],
                    'year': year,
                    'qnum': qnum,
                    'modified_on': fmodified_on})
    reports.sort(key=lambda i: i['year'] + i['qnum'])

    context.update({
        'entity': entity,
        'reports': reports
    })

    cluster = Cluster.get_or_none("malaria_monthly_routine")
    context.update(entity_browser_context(
        root=root, selected_entity=entity,
        full_lineage=['country', 'health_region',
                      'health_district', 'health_center'],
        cluster=cluster))

    return render(request,
                  kwargs.get('template_name',
                             'malaria/quarter_reports_list.html'),
                  context)
