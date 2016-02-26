#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim: ai ts=4 sts=4 et sw=4 nu

from __future__ import (unicode_literals, absolute_import,
                        division, print_function)
import copy

from django.utils.translation import ugettext_lazy as _
from snisi_core.indicators import (IndicatorTable, Indicator,
                                   gen_report_indicator)
from snisi_cataract.models import CATMissionR, AggCATMissionR


class CATMissionIndicator(Indicator):
    INDIVIDUAL_CLS = CATMissionR
    AGGREGATED_CLS = AggCATMissionR

    def should_yesno(self):
        return False

    def total_reports_for(self, field):
        value = 0
        for report in self.reports:
            value += getattr(report.casted(), field, 0)
        return value


class ReportSumDataMixin(object):
    report_field = None

    def _compute(self):
        value = 0
        for report in self.reports:
            value += getattr(report.casted(), self.report_field, 0)
        return value


def gen_reportsum_indicator(field,
                            name=None,
                            report_cls=None,
                            base_indicator_cls=Indicator):

    class GenericReportIndicator(ReportSumDataMixin, base_indicator_cls):
        pass

    cls = copy.copy(GenericReportIndicator)
    cls.report_field = field
    cls.name = name if name else report_cls.field_name(field) \
        if report_cls is not None else None
    return cls

gen_shortcut = lambda field, label=None: gen_report_indicator(
    field, name=label, report_cls=CATMissionR,
    base_indicator_cls=CATMissionIndicator)

gen_sum_shortcut = lambda field, label=None: gen_reportsum_indicator(
    field, name=label, report_cls=AggCATMissionR,
    base_indicator_cls=CATMissionIndicator)


class NbCATMissions(CATMissionIndicator):
    name = "Nombre de missions"

    def _compute(self):
        print(self.reports)
        return sum([r.casted().indiv_sources.count()
                    for r in self.reports])


class MissionDataSummary(IndicatorTable):

    name = "Tableau 1"
    title = " "
    caption = ("Données cumulatives mensuelles ; chirurgies catracte")
    rendering_type = 'table'

    INDICATORS = [
        NbCATMissions,
        gen_sum_shortcut('nb_surgery_reports'),
        gen_sum_shortcut('nb_surgery_male'),
        gen_sum_shortcut('nb_surgery_female'),
        gen_sum_shortcut('nb_surgery_right_eye'),
        gen_sum_shortcut('nb_surgery_left_eye'),
        gen_sum_shortcut('nb_age_under_15'),
        gen_sum_shortcut('age_between_15_18',
                         _("Nb. surgeries Patient aged 15-18")),
        gen_sum_shortcut('age_between_18_20',
                         _("Nb. surgeries Patient aged 18-20")),
        gen_sum_shortcut('age_between_20_25',
                         _("Nb. surgeries Patient aged 20-25")),
        gen_sum_shortcut('age_between_25_30',
                         _("Nb. surgeries Patient aged 25-30")),
        gen_sum_shortcut('age_between_30_35',
                         _("Nb. surgeries Patient aged 30-35")),
        gen_sum_shortcut('age_between_35_40',
                         _("Nb. surgeries Patient aged 35-40")),
        gen_sum_shortcut('age_between_40_45',
                         _("Nb. surgeries Patient aged 40-45")),
        gen_sum_shortcut('age_between_45_50',
                         _("Nb. surgeries Patient aged 45-50")),
        gen_sum_shortcut('nb_age_over_50'),
    ]


class CumulativeSurgeryData(IndicatorTable):

    name = "Figure 2"
    title = " "
    caption = ("Évolution des chirurgies catracte")
    rendering_type = 'graph'
    graph_type = 'areaspline'

    INDICATORS = [
        gen_sum_shortcut('nb_surgery_reports', "Cumul chirurgies"),
        gen_sum_shortcut('nb_surgery_right_eye', "Cumul chirurgies OD"),
        gen_sum_shortcut('nb_surgery_left_eye', "Cumul chirurgies OG"),
    ]
