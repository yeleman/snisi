#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim: ai ts=4 sts=4 et sw=4 nu

from __future__ import (unicode_literals, absolute_import,
                        division, print_function)

from snisi_core.models.Projects import Domain

PROJECT_BRAND = "PNLC"
DOMAIN_SLUG = 'trachoma'


def get_domain():
    return Domain.get_or_none(DOMAIN_SLUG)
