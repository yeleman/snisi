#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim: ai ts=4 sts=4 et sw=4 nu

from __future__ import (unicode_literals, absolute_import,
                        division, print_function)
import random

from snisi_tools.ident import checkdigit_for

from snisi_core.models.Entities import HealthEntity

CHARACTERS_POOL = '23456789ABCDEFGHJKMNPRSTWXYZ'
ID_LENGTH = 3


def base_random_id():
    return ''.join([random.choice(CHARACTERS_POOL) for i in range(ID_LENGTH)])


def full_random_id():
    base = base_random_id()
    check_digit = checkdigit_for(base)
    return "{base}{cdigit}".format(base=base, cdigit=check_digit)


def get_unused_ident():
    nb_entities = HealthEntity.objects.count()
    attempts = 0
    while attempts <= nb_entities + 10:
        attempts += 1
        ident = full_random_id()
        if HealthEntity.objects.filter(slug=ident).count():
            continue
        return ident
    raise Exception("Unable to compute a free identifier for HealthEntity.")
