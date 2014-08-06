#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim: ai ts=4 sts=4 et sw=4 nu

from __future__ import (unicode_literals, absolute_import,
                        division, print_function)
import copy

from snisi_core.indicators import (IndicatorTable, Indicator,
                                   gen_report_indicator)
from snisi_trachoma.models import TTBacklogMissionR


class TTMissionIndicator(Indicator):
    INDIVIDUAL_CLS = TTBacklogMissionR
    AGGREGATED_CLS = TTBacklogMissionR

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
    field, name=label, report_cls=TTBacklogMissionR,
    base_indicator_cls=TTMissionIndicator)

gen_sum_shortcut = lambda field, label=None: gen_reportsum_indicator(
    field, name=label, report_cls=TTBacklogMissionR,
    base_indicator_cls=TTMissionIndicator)


class NbTTMissions(TTMissionIndicator):
    name = "Nombre de missions"

    def _compute(self):
        return len(self.reports)

# class NBTTConsultations(TTMissionIndicator):
#     name = "Consultés Homme"
#     def _compute(self):
#         return self.total_reports_for('consultation_male')


class MissionDataSummary(IndicatorTable):
    """ """

    name = "Tableau 1"
    title = " "
    caption = ("Données cumulatives mensuelles ; suivi du Backlog TT")
    rendering_type = 'table'

    INDICATORS = [
        NbTTMissions,
        gen_sum_shortcut('nb_village_reports'),
        gen_sum_shortcut('consultation_male'),
        gen_sum_shortcut('consultation_female'),
        gen_sum_shortcut('surgery_male'),
        gen_sum_shortcut('surgery_female'),
        gen_sum_shortcut('refusal_male'),
        gen_sum_shortcut('refusal_female'),
        gen_sum_shortcut('recidivism_male'),
        gen_sum_shortcut('recidivism_female'),
        gen_sum_shortcut('nb_community_assistance'),

    ]


class ConsultationGrandTotal(TTMissionIndicator):
    name = "Cumul Opérations"

    def _compute(self):
        return len(self.reports)


class CumulativeBacklogData(IndicatorTable):
    """ """

    name = "Figure 2"
    title = " "
    caption = ("Évolution des opérations TT")
    rendering_type = 'graph'
    graph_type = 'areaspline'

    INDICATORS = [
        gen_sum_shortcut('consultation', "Cumul consultation"),
        gen_sum_shortcut('surgery', "Cumul opérés"),
        gen_sum_shortcut('redicivism', "Cumul récidives"),
    ]
