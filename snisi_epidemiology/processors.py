#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim: ai ts=4 sts=4 et sw=4 nu

from __future__ import (unicode_literals, absolute_import,
                        division, print_function)
import logging
import datetime

from django.utils import timezone

from snisi_epidemiology.models import EpidemiologyR, EpiWeekPeriod
from snisi_epidemiology.views import nb_cases_for

logger = logging.getLogger(__name__)


def default_context():
    periods = EpiWeekPeriod.all_from(
        EpiWeekPeriod.find_create_by_date(
            timezone.now() - datetime.timedelta(days=15)))

    return {
        'mado_nb_cases': nb_cases_for(periods, EpidemiologyR),
        'mado_level': 'danger'
        if nb_cases_for(periods, EpidemiologyR, 'deaths')
        else 'warning'
    }
