#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim: ai ts=4 sts=4 et sw=4 nu

from __future__ import (unicode_literals, absolute_import,
                        division, print_function)

from snisi_core.indicators import Indicator, gen_report_indicator
from snisi_malaria.models import MalariaR, AggMalariaR


class MalariaIndicator(Indicator):
    INDIVIDUAL_CLS = MalariaR
    AGGREGATED_CLS = AggMalariaR

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

gen_shortcut = lambda field, label=None: gen_report_indicator(field,
                                                  name=label,
                                                  report_cls=MalariaR,
                                                  base_indicator_cls=MalariaIndicator)

gen_shortcut_agg = lambda field, label=None: gen_report_indicator(field,
                                                  name=label,
                                                  report_cls=AggMalariaR,
                                                  base_indicator_cls=MalariaIndicator)