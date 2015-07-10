#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim: ai ts=4 sts=4 et sw=4 nu

from __future__ import (unicode_literals, absolute_import,
                        division, print_function)
import logging

from snisi_core.indicators import IndicatorTable, Indicator
from snisi_nutrition.models.Weekly import WeeklyNutritionR, AggWeeklyNutritionR
from snisi_core.indicators import (
    IndicatorTable, em, SummaryForEntitiesTable, ReportDataMixin,
    DataIsMissing)
from snisi_nutrition.indicators.common import (
    IndicatorTableWithEntities,
    NutritionIndicator, shoudl_show, gen_fixed_entity_indicator)
from snisi_core.indicators import is_ref, ref_is, hide
from snisi_core.models.Reporting import SNISIReport

logger = logging.getLogger(__name__)


class WeekNutritionIndicator(Indicator):
    INDIVIDUAL_CLS = WeeklyNutritionR
    AGGREGATED_CLS = AggWeeklyNutritionR

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

    def all_hc_func_values(self, subreport, func, *params):
        return [getattr(getattr(r, subreport), func)(*params)
                for r in self.report.indiv_sources.all()]


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
                return 1 if self.report.arrival_status == SNISIReport.ON_TIME \
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
    # add_percentage = True

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


class WeekNbSourceReportsExpected(WeekNutritionIndicator):
    name = "Nombre de rapports attendus"

    def _compute(self):
        if self.is_hc():
            return 1 if self._expected else 0
        return getattr(self.report, 'nb_source_reports_expected', 0)


class WeekNbSourceReportsArrived(WeekNutritionIndicator):
    name = "Nombre de rapports reçus"

    def _compute(self):
        if self.is_hc():
            return 1 if self._expected.satisfied else 0
        return getattr(self.report, 'nb_source_reports_arrived', 0)


class WeekNbSourceReportsArrivedOnTime(WeekNutritionIndicator):
    name = "Nombre de rapports reçus à temps"

    def _compute(self):
        if self.is_hc():
            if self._expected.satisfied:
                return 1 if self.report.arrival_status == SNISIReport.ON_TIME \
                    else 0
            else:
                return 0
        return getattr(self.report, 'nb_source_reports_arrived_on_time', 0)


class WeekTableauPromptitudeRapportage(IndicatorTable):

    name = "Tableau 2"
    title = ""
    caption = ("Pourcentage de structures ayant transmis leurs formulaires "
               "de collecte hebdo dans les délais prévus")
    rendering_type = 'table'
    # add_percentage = True

    INDICATORS = [
        is_ref(WeekNbSourceReportsExpected),
        ref_is(0)(WeekNbSourceReportsArrived),
        ref_is(0)(WeekNbSourceReportsArrivedOnTime),
    ]


class WeekFigurePromptitudeRapportage(IndicatorTable):

    name = "Figure 2"
    title = ""
    caption = ("Évolution de la promptitude de la notification hebdo")
    rendering_type = 'graph'
    graph_type = 'spline'
    as_percentage = True

    INDICATORS = [
        hide(is_ref(WeekNbSourceReportsExpected)),
        ref_is(0)(WeekNbSourceReportsArrived),
        ref_is(0)(WeekNbSourceReportsArrivedOnTime),
    ]
