#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim: ai ts=4 sts=4 et sw=4 nu

from __future__ import (unicode_literals, absolute_import,
                        division, print_function)
import logging

import numpy

from snisi_core.models.Projects import Cluster
# from snisi_core.models.Reporting import ExpectedReporting
# from snisi_tools.caching import descendants_slugs
from snisi_core.indicators import Indicator, gen_report_indicator
from snisi_vacc.models import VaccCovR, AggVaccCovR
from snisi_tools.misc import import_path

logger = logging.getLogger(__name__)
cluster = Cluster.get_or_none("major_vaccine_monthly")
excludes = ['VaccinationIndicator', 'Indicator']


class VaccinationIndicator(Indicator):
    INDIVIDUAL_CLS = VaccCovR
    AGGREGATED_CLS = AggVaccCovR

    def is_hc(self):
        ''' whether at HealthCenter/Source level or not (above) '''
        return self.entity.type.slug == 'health_center'

    def should_yesno(self):
        return self.is_hc()

    def sum_on_hc(self, field):
        return sum(self.all_hc_values(field))

    def all_hc_values(self, field):
        return [getattr(r, field, None)
                for r in self.report.indiv_sources.all()]

    def sources_average(self, field):
        return float(numpy.mean(self.all_hc_values(field)))

    def inverse(self, value):
        if value < 0:
            return float(1 + numpy.abs(value))
        else:
            return float(1 - value)

gen_shortcut = lambda field, label=None: gen_report_indicator(
    field, name=label, report_cls=VaccCovR,
    base_indicator_cls=VaccinationIndicator)

gen_shortcut_agg = lambda field, label=None: gen_report_indicator(
    field, name=label, report_cls=AggVaccCovR,
    base_indicator_cls=VaccinationIndicator)


class BCGCoverage(VaccinationIndicator):
    name = ("Taux de couverture BCG")
    is_ratio = True
    is_geo_friendly = True
    geo_section = "Couverture"
    is_yesno = False

    def _compute(self):
        if self.is_hc():
            return self.report.bcg_coverage
        else:
            return self.sources_average('bcg_coverage')


class Polio3Coverage(VaccinationIndicator):
    name = ("Taux de couverture Penta-3")
    is_ratio = True
    is_geo_friendly = True
    geo_section = "Couverture"
    is_yesno = False

    def _compute(self):
        if self.is_hc():
            return self.report.polio3_coverage
        else:
            return self.sources_average('polio3_coverage')


class MeaslesCoverage(VaccinationIndicator):
    name = ("Taux de couverture VAR-1")
    is_ratio = True
    is_geo_friendly = True
    geo_section = "Couverture"
    is_yesno = False

    def _compute(self):
        if self.is_hc():
            return self.report.measles_coverage
        else:
            return self.sources_average('measles_coverage')


class NonAbandonmentRate(VaccinationIndicator):
    name = ("Taux de poursuite (non-abandon) Penta-1 / Penta-3")
    is_ratio = True
    is_geo_friendly = True
    geo_section = "Abandons"
    is_yesno = False

    def _compute(self):
        if self.is_hc():
            return self.inverse(self.report.polio3_abandonment_rate)
        else:
            return self.inverse(
                self.sources_average('polio3_abandonment_rate'))


def is_indicator(module, member, only_geo=False):
    ind = get_indicator(module, member)
    if not getattr(ind, 'SNISI_INDICATOR', None) or member in excludes:
        return False
    if only_geo and not getattr(ind, 'is_geo_friendly', None):
        return False
    return True


def get_indicator(module, member):
    if module is None:
        return member
    return getattr(module, member)


def get_geo_indicators():
    print(__package__)
    indicators = {}
    # section = get_section("map")
    section = import_path('snisi_vacc.indicators')
    for indicator_name in dir(section):
        if not is_indicator(section, indicator_name, True):
            continue
        indicator = import_path('snisi_vacc.indicators.{}'
                                .format(indicator_name))
        geo_section = getattr(indicator, 'geo_section', None)
        if geo_section not in indicators.keys():
            indicators.update({geo_section: []})
        spec = indicator.spec()
        spec.update({'slug': indicator.__name__})
        indicators[geo_section].append(spec)

    return indicators
