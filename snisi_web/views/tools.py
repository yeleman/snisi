#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim: ai ts=4 sts=4 et sw=4 nu

from __future__ import (unicode_literals, absolute_import,
                        division, print_function)
import logging

logger = logging.getLogger(__name__)


def withCORS(r):
    r['Access-Control-Allow-Origin'] = "*"
    r['Access-Control-Allow-Credentials'] = "false"
    return r
