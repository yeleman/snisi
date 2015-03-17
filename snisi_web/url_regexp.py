#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim: ai ts=4 sts=4 et sw=4 nu

from __future__ import (unicode_literals, absolute_import,
                        division, print_function)
import logging

logger = logging.getLogger(__name__)

RGXP_REPORTCLS = r'(?P<reportcls_slug>[a-zA-Z\_\-0-1]+)'
RGXP_CLUSTER = r'(?P<cluster_slug>[a-zA-Z\_\-0-1\-]+)'
RGXP_ENTITY = r'(?P<entity_slug>[a-zA-Z0-9]+)'
RGXP_RECEIPT = r'(?P<report_receipt>[a-zA-Z\#\-\_\.0-9\/]+)'
RGXP_SECTION = 'section(?P<section_index>[0-9]{1,2}[ab]{0,1})'
RGXP_SUBSECTION = '(?P<sub_section>[a-z\_]*)'

"""
FORMATS:

YEAR:       2013                                [0-9]{4}
MONTH:      01-2013                             [0-9]{2}-[0-9]{4}
QUARTER:    Q1-2013                             Q[1-3]-[0-9]{4}
WEEK:       W1-2013                             W[0-9]{1,2}-[0-9]{4}
DAY:        01-01-2013                          [0-9]{2}-[0-9]{2}-[0-9]{4}
"""
RGXP_PERIOD = (r'(?P<period_str>[0-9]{4}|[0-9]{2}\-[0-9]{4}'
               r'|Q[1-3]\-[0-9]{4}'
               r'|W[0-9]{1,2}\-[0-9]{4}|[0-9]{2}\-[0-9]{2}\-[0-9]{4}'
               r'|nW[0-9]{1,2}\-[0-9]{4}'
               ')/?$')

RGXP_PERIODS = (r'(?P<period_str>'
                r'[0-9]{4}|[0-9]{2}\-[0-9]{4}|Q[1-3]\-[0-9]{4}|'
                r'W[0-9]{1,2}\-[0-9]{4}|[0-9]{2}\-[0-9]{2}\-[0-9]{4}'
                r'_'
                r'[0-9]{4}|[0-9]{2}\-[0-9]{4}|Q[1-3]\-[0-9]{4}|'
                r'W[0-9]{1,2}\-[0-9]{4}|[0-9]{2}\-[0-9]{2}\-[0-9]{4}'
                r')')

RGXP_PERIODS = (r'(?P<perioda_str>[0-9]{4}|[0-9]{2}\-[0-9]{4}'
                r'|Q[1-3]\-[0-9]{4}|W[0-9]{1,2}\-[0-9]{4}'
                r'|[0-9]{2}\-[0-9]{2}\-[0-9]{4})'
                r'_(?P<periodb_str>[0-9]{4}'
                r'|[0-9]{2}\-[0-9]{4}|Q[1-3]\-[0-9]{4}'
                r'|W[0-9]{1,2}\-[0-9]{4}|[0-9]{2}\-[0-9]{2}\-[0-9]{4})')
