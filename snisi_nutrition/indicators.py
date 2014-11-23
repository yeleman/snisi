#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim: ai ts=4 sts=4 et sw=4 nu

from __future__ import (unicode_literals, absolute_import,
                        division, print_function)

from snisi_core.indicators import (IndicatorTable, Indicator,
                                   gen_report_indicator, is_ref, ref_is, hide)
from snisi_nutrition.models.Monthly import NutritionR, AggNutritionR


class NutritionIndicator(Indicator):
    INDIVIDUAL_CLS = NutritionR
    AGGREGATED_CLS = AggNutritionR

    def is_hc(self):
        return self.entity.type.slug == 'health_center'

    def should_yesno(self):
        return self.is_hc()

    def sum_on_hc(self, field):
        return sum(self.all_hc_values(field))

    def all_hc_values(self, field):
        return [getattr(r, field, None)
                for r in self.report.indiv_sources.all()]

    def total_reports_for(self, field):
        value = 0
        for report in self.reports:
            value += getattr(report.casted(), field, 0)
        return value


gen_shortcut = lambda field, label=None: gen_report_indicator(
    field, name=label, report_cls=NutritionR,
    base_indicator_cls=NutritionIndicator)

gen_shortcut_agg = lambda field, label=None: gen_report_indicator(
    field, name=label, report_cls=AggNutritionR,
    base_indicator_cls=NutritionIndicator)


class HealedRate(NutritionIndicator):
    name = "Taux de guérison"
    is_ratio = True

    def _compute(self):
        return self.report.healed_rate


class DeceasedRate(NutritionIndicator):
    name = "Taux de décès"
    is_ratio = True

    def _compute(self):
        return self.report.deceased_rate


class AbandonRate(NutritionIndicator):
    name = "Taux d'abandon"
    is_ratio = True

    def _compute(self):
        return self.report.abandon_rate


class URENIInRate(NutritionIndicator):
    name = "Taux d'admission URENI"
    is_ratio = True

    def _compute(self):
        if not self.report.ureni_report:
            return 0
        return (self.report.ureni_report.grand_total_in
                / self.report.grand_total_in)


class URENASInRate(NutritionIndicator):
    name = "Taux d'admission URENAS"
    is_ratio = True

    def _compute(self):
        if not self.report.urenas_report:
            return 0
        return (self.report.urenas_report.grand_total_in
                / self.report.grand_total_in)


class URENAMInRate(NutritionIndicator):
    name = "Taux d'admission URENAM"
    is_ratio = True

    def _compute(self):
        if not self.report.urenam_report:
            return 0
        return (self.report.urenam_report.grand_total_in
                / self.report.grand_total_in)


class PerformanceIndicators(IndicatorTable):
    """ """

    name = "Tableau 2"
    title = " "
    caption = ("Indicateurs de performance")
    rendering_type = 'table'

    INDICATORS = [
        gen_shortcut('total_out_resp', "Nombre de sorties (hors non-rép.)"),
        gen_shortcut('healed', "Guéris"),
        HealedRate,
        gen_shortcut('deceased', "Décès"),
        DeceasedRate,
        gen_shortcut('abandon', "Abandon"),
        AbandonRate,
        URENIInRate,
        URENASInRate,
    ]


class FigurePerformanceIndicators(IndicatorTable):

    name = "Figure 2"
    title = ""
    caption = ("Évolution des indicateurs de performance")
    rendering_type = 'graph'
    graph_type = 'spline'
    as_percentage = True

    INDICATORS = [
        HealedRate,
        DeceasedRate,
        AbandonRate,
    ]


class NbSourceReportsExpected(NutritionIndicator):
    name = "Nombre de rapports attendus"

    def _compute(self):
        if self.is_hc():
            return 1 if self._expected else 0
        return getattr(self.report, 'nb_source_reports_expected', 0)


class NbSourceReportsArrived(NutritionIndicator):
    name = "Nombre de rapports reçus"

    def _compute(self):
        if self.is_hc():
            return 1 if self._expected.satisfied else 0
        return getattr(self.report, 'nb_source_reports_arrived', 0)


class NbSourceReportsArrivedOnTime(NutritionIndicator):
    name = "Nombre de rapports reçus à temps"

    def _compute(self):
        if self.is_hc():
            if self._expected.satisfied:
                return 1 if self.report.arrival_status == NutritionR.ON_TIME \
                    else 0
            else:
                return 0
        return getattr(self.report, 'nb_source_reports_arrived_on_time', 0)


class TableauPromptitudeRapportage(IndicatorTable):

    name = "Tableau 1"
    title = ""
    caption = ("Pourcentage de structures ayant transmis leurs formulaires "
               "de collecte dans les délais prévus")
    rendering_type = 'table'

    INDICATORS = [
        is_ref(NbSourceReportsExpected),
        ref_is(0)(NbSourceReportsArrived),
        ref_is(0)(NbSourceReportsArrivedOnTime),
    ]


class FigurePromptitudeRapportage(IndicatorTable):

    name = "Figure 1"
    title = ""
    caption = ("Évolution de la promptitude de la notification")
    rendering_type = 'graph'
    graph_type = 'spline'
    as_percentage = True

    INDICATORS = [
        hide(is_ref(NbSourceReportsExpected)),
        ref_is(0)(NbSourceReportsArrived),
        ref_is(0)(NbSourceReportsArrivedOnTime),
    ]
