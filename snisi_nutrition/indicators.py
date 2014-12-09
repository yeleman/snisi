#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim: ai ts=4 sts=4 et sw=4 nu

from __future__ import (unicode_literals, absolute_import,
                        division, print_function)
import copy

from snisi_core.indicators import (IndicatorTable, Indicator,
                                   ReportDataMixin,
                                   gen_report_indicator,
                                   is_ref, ref_is, hide, em)
from snisi_core.models.Entities import Entity
from snisi_core.models.Projects import Cluster
from snisi_tools.caching import json_cache_from_cluster
from snisi_nutrition.models.Monthly import NutritionR, AggNutritionR

cluster = Cluster.get_or_none("nutrition_routine")


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


class SAMHealedRate(NutritionIndicator):
    name = "Taux de guérison"
    is_ratio = True

    def _compute(self):
        return self.report.sam_comp_healed_rate


class SAMDeceasedRate(NutritionIndicator):
    name = "Taux de décès"
    is_ratio = True

    def _compute(self):
        return self.report.sam_comp_deceased_rate


class SAMAbandonRate(NutritionIndicator):
    name = "Taux d'abandon"
    is_ratio = True

    def _compute(self):
        return self.report.sam_comp_abandon_rate


class MAMHealedRate(NutritionIndicator):
    name = "Taux de guérison"
    is_ratio = True

    def _compute(self):
        return self.report.mam_comp_healed_rate


class MAMDeceasedRate(NutritionIndicator):
    name = "Taux de décès"
    is_ratio = True

    def _compute(self):
        return self.report.mam_comp_deceased_rate


class MAMAbandonRate(NutritionIndicator):
    name = "Taux d'abandon"
    is_ratio = True

    def _compute(self):
        return self.report.mam_comp_abandon_rate


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


# SYNTHESE NUT DS
class NouvellesAdmissionsURENAS(ReportDataMixin, NutritionIndicator):

    report_field = 'urenas_report'
    report_sub_field = 'comp_new_cases'
    name = "TOTAL URENAS"


class NouvellesAdmissionsURENI(ReportDataMixin, NutritionIndicator):

    report_field = 'ureni_report'
    report_sub_field = 'comp_new_cases'
    name = "TOTAL URENI"


class NouvellesAdmissionsURENASURENI(NutritionIndicator):
    name = "TOTAL URENI + URENAS"

    def _compute(self):
        return sum([
            getattr(self.report.urenas_report, 'comp_new_cases', 0),
            getattr(self.report.ureni_report, 'comp_new_cases', 0),
            ])


class NouvellesAdmissionsMAS(NouvellesAdmissionsURENASURENI):
    name = "Nouvelles admissions 6-59 mois"


class NouvellesAdmissionsURENAM(ReportDataMixin, NutritionIndicator):

    report_field = 'urenam_report'
    report_sub_field = 'comp_new_cases'
    name = "TOTAL URENAM"


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


class TableNouvellesAdmissionsURENIURENAS(IndicatorTableWithEntities):

    name = "Tableau 1.a"
    title = ""
    caption = ("NOUVELLES ADMISSIONS 6-59 MOIS - URENI/URENAS")
    rendering_type = 'table'

    def build_indicators(self):

        descendants = self.get_descendants()

        indicatorsl = []

        # List of all URENI
        for descendant in descendants:
            if getattr(descendant, 'has_ureni', False):
                ind = gen_fixed_entity_indicator(entity=descendant,
                                                 sub_report='ureni_report',
                                                 field='comp_new_cases')
                indicatorsl.append(ind)

        # Total URENI
        indicatorsl.append(em(NouvellesAdmissionsURENI))

        # List of all URENAS
        for descendant in descendants:
            if getattr(descendant, 'has_urenas', False):
                ind = gen_fixed_entity_indicator(entity=descendant,
                                                 sub_report='urenas_report',
                                                 field='comp_new_cases')
                indicatorsl.append(ind)

        # Total URENAS
        indicatorsl.append(em(NouvellesAdmissionsURENAS))

        # Total URENI + URENAS
        indicatorsl.append(em(NouvellesAdmissionsURENASURENI))

        return indicatorsl


class TableNouvellesAdmissionsURENAM(IndicatorTableWithEntities):

    name = "Tableau 1.b"
    title = ""
    caption = ("NOUVELLES ADMISSIONS 6-59 MOIS - URENAM")
    rendering_type = 'table'

    def build_indicators(self):

        descendants = self.get_descendants()

        indicatorsl = []

        # List of all URENAM
        for descendant in descendants:
            if getattr(descendant, 'has_urenam', False):
                ind = gen_fixed_entity_indicator(entity=descendant,
                                                 sub_report='urenam_report',
                                                 field='comp_new_cases')
                indicatorsl.append(ind)

        # Total URENAM
        indicatorsl.append(em(NouvellesAdmissionsURENAM))

        return indicatorsl


class TableCaseloadSAM(IndicatorTable):

    name = "Tableau 2"
    title = ""
    caption = ("CASELOAD MAS 6-59 MOIS ATTENDU DS")
    rendering_type = 'table'
    add_total = True

    INDICATORS = [
        NouvellesAdmissionsMAS
    ]


class PercentNouvellesAdmissionsURENAS(NouvellesAdmissionsURENAS):
    name = "% ADMISSIONS URENAS"
    is_ratio = True

    def _compute(self):
        return self.report.urenas_report.comp_new_cases \
            / self.report.sam_comp_new_cases


class PercentNouvellesAdmissionsURENI(NouvellesAdmissionsURENI):
    name = "% ADMISSIONS URENI"
    is_ratio = True

    def _compute(self):
        return self.report.ureni_report.comp_new_cases \
            / self.report.sam_comp_new_cases


class TableRepartitionURENIURENAS(IndicatorTable):

    name = "Tableau 3"
    title = ""
    caption = ("% ADMISSIONS 6-59 MOIS URENI/URENAS")
    rendering_type = 'table'
    add_total = True

    INDICATORS = [
        PercentNouvellesAdmissionsURENI,
        PercentNouvellesAdmissionsURENAS,
    ]


class TablePerformanceSAM(IndicatorTable):
    name = "Tableau 4.a"
    title = ""
    caption = ("INDICATEURS PERFORMANCE MAS 6-59 MOIS DS")
    rendering_type = 'table'
    add_total = True

    INDICATORS = [
        SAMDeceasedRate,
        SAMHealedRate,
        SAMAbandonRate,
    ]


class TablePerformanceMAM(IndicatorTable):
    name = "Tableau 4.b"
    title = ""
    caption = ("INDICATEURS PERFORMANCE MAM 6-59 MOIS DS")
    rendering_type = 'table'
    add_total = True

    INDICATORS = [
        MAMDeceasedRate,
        MAMHealedRate,
        MAMAbandonRate,
    ]


class GraphRepartitionURENIURENAS(TableRepartitionURENIURENAS):
    name = "Graphique 1"
    title = ""
    caption = ("Nouvelles admissions")
    add_total = False
    is_percentage = True
    rendering_type = 'graph'
    graph_type = 'column'
    graph_stacking = True


class GraphPerformanceSAM(TablePerformanceSAM):
    name = "Graphique 2.a"
    title = ""
    caption = ("Indicateurs de performance MAS")
    add_total = False
    is_percentage = True
    rendering_type = 'graph'
    graph_type = 'column'
    graph_stacking = True


class GraphPerformanceMAM(TablePerformanceMAM):
    name = "Graphique 2.b"
    title = ""
    caption = ("Indicateurs de performance MAM")
    add_total = False
    is_percentage = True
    rendering_type = 'graph'
    graph_type = 'column'
    graph_stacking = True


# Montly NUT Snthesis

class GraphNouvellesAdmissionsURENIURENAS(IndicatorTableWithEntities):

    name = "Graphique 2"
    title = ""
    caption = ("Nouvelles admissions par URENAS")
    rendering_type = 'graph'
    graph_type = 'column'

    def build_indicators(self):

        descendants = self.get_descendants()

        indicatorsl = []

        # List of all URENAS
        for descendant in descendants:
            if getattr(descendant, 'has_urenas', False):
                ind = gen_fixed_entity_indicator(entity=descendant,
                                                 sub_report='urenas_report',
                                                 field='comp_new_cases')
                indicatorsl.append(ind)

        return indicatorsl
