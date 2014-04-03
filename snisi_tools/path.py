#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim: ai ts=4 sts=4 et sw=4 nu

from __future__ import (unicode_literals, absolute_import,
                        division, print_function)
import logging
import os
import errno
import datetime

from django.utils import timezone

logger = logging.getLogger(__name__)


def mkdir_p(path):
    try:
        os.makedirs(path)
    except OSError as exc: # Python >2.5
        if exc.errno == errno.EEXIST and os.path.isdir(path):
            pass
        else: raise


def modified_on(filepath):
    t = os.path.getmtime(filepath)
    return datetime.datetime.fromtimestamp(t).replace(tzinfo=timezone.utc)
