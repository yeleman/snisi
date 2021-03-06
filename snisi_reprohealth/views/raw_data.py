#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim: ai ts=4 sts=4 et sw=4 nu

from __future__ import (unicode_literals, absolute_import,
                        division, print_function)
import logging

from snisi_web.views.raw_data import browser as web_browser

logger = logging.getLogger(__name__)


def browser(request, entity_slug=None, period_str=None):
    return web_browser(request,
                       cluster_slug='msi_reprohealth_routine',
                       entity_slug=entity_slug,
                       period_str=period_str,
                       template_name='reprohealth/msi_report.html',
                       view_name='msipf_raw_data')
