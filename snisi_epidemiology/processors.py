#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim: ai ts=4 sts=4 et sw=4 nu

from __future__ import (unicode_literals, absolute_import,
                        division, print_function)
import logging
import datetime

from django.utils import timezone

from snisi_epidemiology.models import (
    AggEpidemiologyR, EpiWeekPeriod, EpidemiologyAlertR)
from snisi_epidemiology.views import nb_cases_for

logger = logging.getLogger(__name__)


def old_default_context():
    # TODO: restore EpidemiologyR instead of AggEpidemiologyR
    periods = EpiWeekPeriod.all_from(
        EpiWeekPeriod.find_create_by_date(
            timezone.now() - datetime.timedelta(days=15)))

    mado_nb_cases = nb_cases_for(periods, AggEpidemiologyR)
    if mado_nb_cases:
        level = 'danger' \
            if nb_cases_for(periods, AggEpidemiologyR, 'deaths') else 'warning'
    else:
        level = 'success'

    return {'mado_nb_cases': mado_nb_cases, 'mado_level': level}


def default_context():
    days_ago = datetime.date.today() - datetime.timedelta(days=15)
    alerts = EpidemiologyAlertR.objects.filter(date__gte=days_ago)
    nb_deaths = sum([a.deaths for a in alerts])
    nb_suspected_cases = sum([a.suspected_cases for a in alerts])
    if alerts.count() == 0:
        level = 'success'
    else:
        level = 'warning'
        if nb_deaths > 0:
            level = 'danger'
    return {'mado_nb_cases': nb_suspected_cases, 'mado_level': level}
