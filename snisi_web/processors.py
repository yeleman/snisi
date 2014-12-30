#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim: ai ts=4 sts=4 et sw=4 nu

from __future__ import (unicode_literals, absolute_import,
                        division, print_function)
import logging

from snisi_core import branding as branding_dict
from snisi_core.models.Projects import Domain

logger = logging.getLogger(__name__)


def branding(*args, **kwargs):
    return branding_dict


def default_context(*args, **kwargs):
    context = {}

    # loop through all projects and update context
    for domain in Domain.active.all():
        dflt_ctx = domain.import_from('processors.default_context'
                                      .format(domain.module_path))
        if dflt_ctx is not None:
            context.update(dflt_ctx())

    if 'has_admin' not in context.keys():
        context.update({'has_admin': False})

    return context
