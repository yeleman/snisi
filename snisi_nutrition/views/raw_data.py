#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim: ai ts=4 sts=4 et sw=4 nu

from __future__ import (unicode_literals, absolute_import,
                        division, print_function)
import logging

from snisi_web.views.raw_data import browser as web_browser
from snisi_nutrition.models.Weekly import (
    NutWeekPeriod, WeeklyNutritionR, AggWeeklyNutritionR)

logger = logging.getLogger(__name__)


def browser(request, entity_slug=None, period_str=None):
    return web_browser(request,
                       cluster_slug='nutrition_routine',
                       entity_slug=entity_slug,
                       period_str=period_str,
                       view_name='nutrition_raw_data',
                       template_name='nutrition/nut_report.html')


def weekly_browser(request, entity_slug=None, period_str=None):
    return web_browser(request,
                       cluster_slug='nutrition_routine',
                       entity_slug=entity_slug,
                       period_str=period_str,
                       report_cls=(WeeklyNutritionR, AggWeeklyNutritionR),
                       period_cls=NutWeekPeriod,
                       view_name='nutrition_weekly_raw_data',
                       template_name='nutrition/nut_weekly_report.html')


def weekly_browser_children(request, entity_slug=None, period_str=None):
    return web_browser(request,
                       cluster_slug='nutrition_routine',
                       entity_slug=entity_slug,
                       period_str=period_str,
                       report_cls=(WeeklyNutritionR, AggWeeklyNutritionR),
                       period_cls=NutWeekPeriod,
                       view_name='nutrition_weekly_data',
                       template_name='nutrition/nut_weekly_data.html')
