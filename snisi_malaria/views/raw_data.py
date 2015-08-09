#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim: ai ts=4 sts=4 et sw=4 nu

from __future__ import (unicode_literals, absolute_import,
                        division, print_function)
import logging

from snisi_web.views.raw_data import browser as web_browser
from snisi_malaria.models import AggWeeklyMalariaR
from snisi_core.models.FixedWeekPeriods import (
    FixedMonthFirstWeek, FixedMonthSecondWeek, FixedMonthThirdWeek,
    FixedMonthFourthWeek, FixedMonthFifthWeek)

logger = logging.getLogger(__name__)
period_classes = [
    FixedMonthFirstWeek, FixedMonthSecondWeek,
    FixedMonthThirdWeek, FixedMonthFourthWeek, FixedMonthFifthWeek]


def browser(request, entity_slug=None, period_str=None):
    return web_browser(request,
                       cluster_slug='malaria_monthly_routine',
                       entity_slug=entity_slug,
                       period_str=period_str,
                       view_name='malaria_raw_data',
                       template_name='raw_data.html')


def weekly_browser(request, entity_slug=None, period_str=None):
    try:
        period_cls = period_classes[int(period_str[2]) - 1]
    except:
        period_cls = period_classes[0]
    print("calling weekly browser", entity_slug, period_str, period_cls)
    return web_browser(request,
                       cluster_slug='malaria_weekly_routine',
                       entity_slug=entity_slug,
                       period_str=period_str,
                       period_cls=period_cls,
                       view_name='malaria_weekly_raw_data',
                       template_name='malaria/weekly_report.html')
