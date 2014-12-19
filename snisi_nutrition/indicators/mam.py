#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim: ai ts=4 sts=4 et sw=4 nu

from __future__ import (unicode_literals, absolute_import,
                        division, print_function)
import logging

from snisi_core.indicators import (
    IndicatorTable, em, SummaryForEntitiesTable, ReportDataMixin)
from snisi_nutrition.indicators.common import (
    IndicatorTableWithEntities,
    NutritionIndicator, shoudl_show, gen_fixed_entity_indicator)

logger = logging.getLogger(__name__)


# INDIVIDUAL INDICATORS
class MAMHealedRate(NutritionIndicator):
    name = "Taux de guérison"
    is_ratio = True
    raise_class = True

    def _compute(self):
        return self.report.mam_comp_healed_rate

    def get_class(self):
        return self.GOOD if self.data >= 75 else self.BAD


class MAMDeceasedRate(NutritionIndicator):
    name = "Taux de décès"
    is_ratio = True
    raise_class = True

    def _compute(self):
        return self.report.mam_comp_deceased_rate

    def get_class(self):
        return self.GOOD if self.data < 10 else self.BAD


class MAMAbandonRate(NutritionIndicator):
    name = "Taux d'abandon"
    is_ratio = True
    raise_class = True

    def _compute(self):
        return self.report.mam_comp_abandon_rate

    def get_class(self):
        return self.GOOD if self.data < 15 else self.BAD


class MAMNewCases(ReportDataMixin, NutritionIndicator):

    report_field = 'urenam_report'
    report_sub_field = 'comp_new_cases'
    name = "Nouvelles admissions MAM 6-59 mois"


class URENAMNewCases(MAMNewCases):
    name = "TOTAL URENAM"


class MAMCaseloadTreated(NutritionIndicator):
    name = "% Caseload MAM traité"
    raise_class = True

    def _compute(self):
        # TODO: FIX CASELOAD
        return 28

    def get_class(self):
        return self.GOOD if self.data >= 50 else self.WARNING


# TABLES AND GRAPHS
class URENAMNewCasesTable(IndicatorTableWithEntities):

    name = "MAM"
    caption = ("NOUVELLES ADMISSIONS 6-59 MOIS - URENAM")
    rendering_type = 'table'

    def build_indicators(self):

        descendants = self.get_descendants()

        indicatorsl = []

        # List of all URENAM
        for descendant in descendants:
            if shoudl_show(descendant, 'urenam'):
                ind = gen_fixed_entity_indicator(entity=descendant,
                                                 sub_report='urenam_report',
                                                 field='comp_new_cases')
                indicatorsl.append(ind)

        # Total URENAM
        indicatorsl.append(em(URENAMNewCases))

        return indicatorsl


class MAMNewCasesTable(IndicatorTableWithEntities):

    name = "MAM"
    caption = ("NOUVELLES ADMISSIONS MAM 6-59 MOIS")
    rendering_type = 'table'

    def build_indicators(self):

        descendants = self.get_descendants()

        indicatorsl = []

        # List of all URENI
        for descendant in descendants:
            if shoudl_show(descendant, 'ureni'):
                ind = gen_fixed_entity_indicator(entity=descendant,
                                                 sub_report=None,
                                                 field='mam_comp_new_cases')
                indicatorsl.append(ind)

        # Total URENI + URENAS
        indicatorsl.append(em(MAMNewCases))

        return indicatorsl


class MAMPerformanceTable(IndicatorTable):
    name = "MAM"
    caption = ("INDICATEURS PERFORMANCE 6-59 MOIS DS")
    rendering_type = 'table'
    add_total = True
    is_percentage = True
    use_advanced_rendering = True

    INDICATORS = [
        MAMDeceasedRate,
        MAMHealedRate,
        MAMAbandonRate,
    ]


class MAMPerformanceGraph(MAMPerformanceTable):
    name = "MAM"
    caption = ("Indicateurs de performance")
    add_total = False
    is_percentage = True
    rendering_type = 'graph'
    graph_type = 'column'
    graph_stacking = True


# Montly NUT Snthesis
# SYNTHESE NUT RS

class RSMAMCaseloadTable(IndicatorTable):

    name = "MAM"
    caption = ("Casload MAM 6-59")
    rendering_type = 'table'


class RSMAMPerformance(IndicatorTable):

    name = "MAM"
    caption = ("INDICATEURS DE PERFORMANCE MAM 6-59")
    rendering_type = 'table'


class MAMNewCasesGraph(IndicatorTable):

    name = "MAM"
    caption = ("Nouvelles admissions MAM")
    rendering_type = 'graph'
    graph_type = 'column'

    INDICATORS = [
        MAMNewCases,
    ]


class MAMCaseloadTreatedGraph(IndicatorTable):

    name = "MAM"
    caption = ("% CASELOAD MAM TRAITÉ")
    rendering_type = 'graph'
    graph_type = 'column'

    INDICATORS = [
        MAMCaseloadTreated
    ]


class MAMNewCasesByDS(SummaryForEntitiesTable):
    name = "MAM"
    caption = ("Nouvelles admissions MAM par DS")
    rendering_type = 'graph'
    graph_type = 'column'

    INDICATORS = [
        MAMNewCases
    ]


class MAMPerformanceByDS(SummaryForEntitiesTable):
    name = "MAM"
    caption = ("Indicateurs de performance MAM par DS")
    add_total = False
    is_percentage = True
    rendering_type = 'graph'
    graph_type = 'column'
    graph_stacking = True

    INDICATORS = [
        MAMDeceasedRate,
        MAMHealedRate,
        MAMAbandonRate,
    ]


class MAMCaseloadTreatedByDS(SummaryForEntitiesTable):
    name = "MAM"
    caption = ("% caseload MAM traité par DS")
    rendering_type = 'graph'
    graph_type = 'column'
    is_percentage = True

    INDICATORS = [
        MAMCaseloadTreated
    ]
