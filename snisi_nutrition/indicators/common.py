#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim: ai ts=4 sts=4 et sw=4 nu

from __future__ import (unicode_literals, absolute_import,
                        division, print_function)
import copy

from snisi_core.indicators import (IndicatorTable, Indicator,
                                   ReportDataMixin,
                                   gen_report_indicator,
                                   is_ref, ref_is, hide)
from snisi_core.models.Entities import Entity
from snisi_core.models.Projects import Cluster
from snisi_tools.caching import json_cache_from_cluster
from snisi_nutrition.models.Monthly import NutritionR, AggNutritionR

cluster = Cluster.get_or_none("nutrition_routine")


def shoudl_show(e, uren):
        return e.type.slug != 'health_center' or \
            getattr(e, 'has_{}'.format(uren), False)


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


def gen_fixed_entity_indicator(entity, field, sub_report=None):

    class GenericReportIndicator(ReportDataMixin, NutritionIndicator):
        pass

    cls = copy.copy(GenericReportIndicator)
    cls.__name__ = str("{}_{}_{}".format(sub_report,
                                         field,
                                         entity.slug.lower()))
    if sub_report:
        cls.report_field = sub_report
        cls.report_sub_field = field
    else:
        cls.report_field = field
    cls.name = entity.display_name()
    cls.fixed_entity = entity
    return cls


class IndicatorTableWithEntities(IndicatorTable):
    def get_descendants(self):
        return [Entity.get_or_none(e['slug']) for e
                in json_cache_from_cluster(cluster).get(self.entity.slug)]


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


class PromptnessReportingTable(IndicatorTable):

    name = "Rapportage"
    caption = ("Pourcentage de structures ayant transmis leurs formulaires "
               "de collecte dans les délais prévus")
    rendering_type = 'table'

    INDICATORS = [
        is_ref(NbSourceReportsExpected),
        ref_is(0)(NbSourceReportsArrived),
        ref_is(0)(NbSourceReportsArrivedOnTime),
    ]


class PromptnessReportingFigure(IndicatorTable):

    name = "Rapportage"
    caption = ("Évolution de la promptitude de la notification")
    rendering_type = 'graph'
    graph_type = 'spline'
    as_percentage = True

    INDICATORS = [
        hide(is_ref(NbSourceReportsExpected)),
        ref_is(0)(NbSourceReportsArrived),
        ref_is(0)(NbSourceReportsArrivedOnTime),
    ]


class RSCompletionTable(IndicatorTable):

    name = "Rapportage"
    caption = ("RAPPORTS MENSUELS TRANSMIS")
    rendering_type = 'table'
