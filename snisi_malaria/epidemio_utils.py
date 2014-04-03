#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim: ai ts=4 sts=4 et sw=4 nu

from __future__ import (unicode_literals, absolute_import,
                        division, print_function)
import logging
import json
import numpy

from snisi_core.models.Periods import MonthPeriod
from snisi_malaria.models import AggEpidemioMalariaR

logger = logging.getLogger(__name__)


def get_threshold(entity, from_year, month):

    # load past notified cases fron JSON fixture
    past_notified_cases = json.load(
        open('snisi_malaria/fixtures/past_notified_cases.json'))

    def _notified_cases_from_matrix(entity, year, month):
        try:
            return past_notified_cases.get(entity.slug).get(str(year))[month - 1]
        except:
            return None

    def _notified_cases_from_db(entity, year, month):
        period = MonthPeriod.find_create_from(year, month, dont_create=True)
        try:
            report = AggEpidemioMalariaR.objects.get(entity=entity, period=period)
        except AggEpidemioMalariaR.DoesNotExist:
            return None

        return getattr(report, 'total_confirmed_malaria_cases')

    def _notified_cases(entity, year, month):
        nc = _notified_cases_from_db(entity, year, month)
        if nc is None:
            return _notified_cases_from_matrix(entity, year, month)

    # list of the last 5 years
    years = range(from_year -5, from_year)

    # a year:value dict of values for this month over the last 5 years
    month_values = {year: _notified_cases(entity, year, month) for year in years}

    # missing one data. can't calculate the threshold
    if None in month_values.values():
        return None

    # average notified cases for this month over last 5 years
    average = numpy.mean([month_values.get(year) for year in years])

    # deviation between notifiec cases and the average for that month over 5 years
    deviations = [month_values.get(year) - average for year in years]

    # square roots of notified cases for that month over last 5 years
    squares = [numpy.square(dev) for dev in deviations]

    squares_sum = sum(squares)

    fourth_of_squares_sum = squares_sum / 4

    sqrt_of_fourth = numpy.sqrt(numpy.absolute(fourth_of_squares_sum))

    return int(average + (2 * sqrt_of_fourth))

