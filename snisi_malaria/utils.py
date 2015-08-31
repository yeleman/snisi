#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim: ai ts=4 sts=4 et sw=4 nu

from __future__ import (unicode_literals, absolute_import,
                        division, print_function)
import logging

logger = logging.getLogger(__name__)


def weekdaynum_for_datetime(adatetime):
    day = adatetime.day
    if day <= 7:
        return day
    return day % 7 or 7
