#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim: ai ts=4 sts=4 et sw=4 nu

from __future__ import (unicode_literals, absolute_import,
                        division, print_function)

from snisi_core.indicators import (IndicatorTable, Indicator,
                                   gen_report_indicator)
from snisi_reprohealth.models.PFActivities import (PFActivitiesR,
                                                   AggPFActivitiesR)


class PFActivitiesIndicator(Indicator):
    INDIVIDUAL_CLS = PFActivitiesR
    AGGREGATED_CLS = AggPFActivitiesR

    def should_yesno(self):
        return False

    def total_reports_for(self, field):
        value = 0
        for report in self.reports:
            value += getattr(report.casted(), field, 0)
        return value


gen_shortcut = lambda field, label=None: gen_report_indicator(
    field, name=label, report_cls=PFActivitiesR,
    base_indicator_cls=PFActivitiesIndicator)


class FPSummary(IndicatorTable):
    """ """

    name = "Tableau 1"
    title = " "
    caption = ("Statistiques des services PF")

    INDICATORS = [
        gen_shortcut('total_clients', "Total clients"),
        gen_shortcut('new_clients', "Total clients PF première fois"),
        gen_shortcut('total_cap', "Total CAP"),
        gen_shortcut('hiv_tests', "Total tests VIH"),
        gen_shortcut('under25_visits', "Total clients moins de 25ans"),
        gen_shortcut('intrauterine_devices', "Total DIU"),
    ]
