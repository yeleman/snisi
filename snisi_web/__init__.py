#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim: ai ts=4 sts=4 et sw=4 nu

from __future__ import (unicode_literals, absolute_import,
                        division, print_function)

from snisi_core import branding


def default_context(*args, **kwargs):
    context = {}
    context.update(branding)
    return context
