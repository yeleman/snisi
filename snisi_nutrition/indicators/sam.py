#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim: ai ts=4 sts=4 et sw=4 nu

from __future__ import (unicode_literals, absolute_import,
                        division, print_function)
import logging

from snisi_core.indicators import (
    IndicatorTable, em, SummaryForEntitiesTable, ReportDataMixin,
    DataIsMissing)
from snisi_nutrition.indicators.common import (
    IndicatorTableWithEntities,
    NutritionIndicator, shoudl_show, gen_fixed_entity_indicator)
from snisi_nutrition.models.Caseload import ExpectedCaseload
from snisi_nutrition.utils import get_caseload_completion_for

logger = logging.getLogger(__name__)


class SAMHealedRate(NutritionIndicator):
    name = "Taux de guérison"
    is_ratio = True
    raise_class = True
    is_geo_friendly = True
    geo_section = "Performances MAS"

    def _compute(self):
        return self.report.sam_comp_healed_rate

    def get_class(self):
        return self.GOOD if self.data >= 75 else self.BAD


class SAMDeceasedRate(NutritionIndicator):
    name = "Taux de décès"
    is_ratio = True
    raise_class = True
    is_geo_friendly = True
    geo_section = "Performances MAS"

    def _compute(self):
        return self.report.sam_comp_deceased_rate

    def get_class(self):
        return self.GOOD if self.data < 10 else self.BAD


class SAMAbandonRate(NutritionIndicator):
    name = "Taux d'abandon"
    is_ratio = True
    raise_class = True
    is_geo_friendly = True
    geo_section = "Performances MAS"

    def _compute(self):
        return self.report.sam_comp_abandon_rate

    def get_class(self):
        return self.GOOD if self.data < 15 else self.BAD


# SYNTHESE NUT DS
class URENASNewCases(ReportDataMixin, NutritionIndicator):

    report_field = 'urenas_report'
    report_sub_field = 'comp_new_cases'
    name = "TOTAL URENAS"


class URENINewCases(ReportDataMixin, NutritionIndicator):

    report_field = 'ureni_report'
    report_sub_field = 'comp_new_cases'
    name = "TOTAL URENI"


class URENASNewCasesURENI(NutritionIndicator):
    name = "TOTAL URENI + URENAS"

    def _compute(self):
        return sum([
            getattr(self.report.urenas_report, 'comp_new_cases', 0),
            getattr(self.report.ureni_report, 'comp_new_cases', 0),
            ])


class SAMNewCases(URENASNewCasesURENI):
    name = "Nouvelles admissions MAS 6-59 mois"


class SAMCaseloadExpected(NutritionIndicator):
    name = "Caseload MAS attendu"

    def _compute(self):
        try:
            return ExpectedCaseload.get_or_none_from(
                year=self.period.start_on.year,
                entity_slug=self.entity.slug).u59o6_sam
        except:
            raise DataIsMissing


class SAMCaseloadTreated(NutritionIndicator):
    name = "Caseload MAS traité"

    def _compute(self):
        return get_caseload_completion_for(period=self.period,
                                           entity=self.entity,
                                           uren='sam')


class SAMCaseloadTreatedRate(NutritionIndicator):
    name = "% Caseload MAS traité"
    raise_class = True
    is_ratio = True
    is_geo_friendly = True
    geo_section = "Performances MAS"

    def _compute(self):
        expected = SAMCaseloadExpected(
            entity=self.entity,
            period=self.period).data
        treated = SAMCaseloadTreated(
            entity=self.entity,
            period=self.period).data
        try:
            return treated / expected
        except:
            return 0

    def get_class(self):
        return self.GOOD if self.data >= .50 else self.WARNING


class URENASNewCasesRate(URENASNewCases):
    name = "% ADMISSIONS URENAS"
    is_ratio = True
    raise_class = True

    def _compute(self):
        return self.report.urenas_report.comp_new_cases \
            / self.report.sam_comp_new_cases

    def get_class(self):
        return self.GOOD if self.data >= 80 and self.data <= 90 \
            else self.BAD


class URENINewCasesRate(URENINewCases):
    name = "% ADMISSIONS URENI"
    is_ratio = True
    raise_class = True

    def _compute(self):
        return self.report.ureni_report.comp_new_cases \
            / self.report.sam_comp_new_cases

    def get_class(self):
        return self.GOOD if self.data >= 10 and self.data <= 20 \
            else self.BAD


class URENIURENASNewCasesTable(IndicatorTableWithEntities):

    name = "MAS"
    caption = ("NOUVELLES ADMISSIONS 6-59 MOIS - URENI/URENAS")
    rendering_type = 'table'

    def build_indicators(self):

        descendants = self.get_descendants()

        indicatorsl = []

        # List of all URENI
        for descendant in descendants:
            if shoudl_show(descendant, 'ureni'):
                ind = gen_fixed_entity_indicator(entity=descendant,
                                                 sub_report='ureni_report',
                                                 field='comp_new_cases')
                indicatorsl.append(ind)

        # Total URENI
        indicatorsl.append(em(URENINewCases))

        # List of all URENAS
        for descendant in descendants:
            if shoudl_show(descendant, 'urens'):
                ind = gen_fixed_entity_indicator(entity=descendant,
                                                 sub_report='urenas_report',
                                                 field='comp_new_cases')
                indicatorsl.append(ind)

        # Total URENAS
        indicatorsl.append(em(URENASNewCases))

        # Total URENI + URENAS
        indicatorsl.append(em(URENASNewCasesURENI))

        return indicatorsl


class SAMNewCasesTable(IndicatorTableWithEntities):

    name = "MAS"
    caption = ("NOUVELLES ADMISSIONS 6 - 59 MOIS")
    rendering_type = 'table'

    def build_indicators(self):

        descendants = self.get_descendants()

        indicatorsl = []

        # List of all URENI
        for descendant in descendants:
            if shoudl_show(descendant, 'ureni'):
                ind = gen_fixed_entity_indicator(entity=descendant,
                                                 sub_report=None,
                                                 field='sam_comp_new_cases')
                indicatorsl.append(ind)

        # Total URENI + URENAS
        indicatorsl.append(em(SAMNewCases))

        return indicatorsl


class SAMCaseloadTable(IndicatorTable):

    name = "MAS"
    caption = ("CASELOAD MAS 6-59 MOIS ATTENDU")
    rendering_type = 'table'
    add_total = True
    use_advanced_rendering = True

    INDICATORS = [
        SAMNewCases,
        SAMCaseloadTreated
    ]


class URENIURENASRepartitionTable(IndicatorTable):

    name = "MAS"
    caption = ("% ADMISSIONS URENI/URENAS 6-59 MOIS")
    rendering_type = 'table'
    add_total = True
    use_advanced_rendering = True

    INDICATORS = [
        URENINewCasesRate,
        URENASNewCasesRate,
    ]


class SAMPerformanceTable(IndicatorTable):
    name = "MAS"
    caption = ("INDICATEURS PERFORMANCE 6-59 MOIS")
    rendering_type = 'table'
    add_total = True
    use_advanced_rendering = True

    INDICATORS = [
        SAMDeceasedRate,
        SAMHealedRate,
        SAMAbandonRate,
    ]


class URENIURENASRepartitionGraph(URENIURENASRepartitionTable):
    name = "MAS"
    caption = ("Proportion nouvelles admissions Ureni/Urenas")
    add_total = False
    is_percentage = True
    rendering_type = 'graph'
    graph_type = 'column'
    graph_stacking = True


class URENASNewCasesByHC(SummaryForEntitiesTable):
    name = "MAS"
    caption = ("Nouvelles admissions par URENAS")
    add_total = False
    rendering_type = 'graph'
    graph_type = 'column'

    def get_descendants(self):
        return sorted(self.entity.casted().get_health_centers(),
                      key=lambda x: x.name)

    INDICATORS = [
        URENASNewCases
    ]


class SAMPerformanceGraph(SAMPerformanceTable):
    name = "MAS"
    caption = ("Indicateurs de performance")
    add_total = False
    is_percentage = True
    rendering_type = 'graph'
    graph_type = 'column'
    graph_stacking = True


class URENIURENASNewCasesTableWithEntities(IndicatorTableWithEntities):

    name = "MAS"
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


# SYNTHESE NUT RS
class RSSAMCaseloadTable(IndicatorTable):

    name = "MAS"
    caption = ("Casload MAS 6-59")
    rendering_type = 'table'


class RSSAMRepartition(IndicatorTable):

    name = "MAS"
    caption = ("Répartition MAS 6-59")
    rendering_type = 'table'


class RSSAMPerformance(IndicatorTable):

    name = "MAS"
    caption = ("INDICATEURS DE PERFORMANCE MAS 6-59")
    rendering_type = 'table'


class SAMNewCasesGraph(IndicatorTable):

    name = "MAS"
    caption = ("Nouvelles admissions MAS")
    rendering_type = 'graph'
    graph_type = 'column'

    INDICATORS = [
        SAMNewCases,
    ]


class SAMCaseloadTreatedGraph(IndicatorTable):

    name = "MAS"
    caption = ("% CASELOAD MAS TRAITÉ")
    rendering_type = 'graph'
    graph_type = 'column'
    is_percentage = True

    INDICATORS = [
        SAMCaseloadTreatedRate
    ]


class SAMNewCasesByDS(SummaryForEntitiesTable):
    name = "MAS"
    caption = ("Nouvelles admissions MAS par DS")
    rendering_type = 'graph'
    graph_type = 'column'

    INDICATORS = [
        SAMNewCases
    ]


class SAMRepartitionByDS(SummaryForEntitiesTable):
    name = "MAS"
    caption = ("Proportion URENI/URENAS par DS")
    rendering_type = 'graph'
    graph_type = 'column'
    is_percentage = True
    graph_stacking = True

    INDICATORS = [
        URENINewCasesRate,
        URENASNewCasesRate
    ]


class SAMPerformanceByDS(SummaryForEntitiesTable):
    name = "MAS"
    caption = ("Indicateurs de performance MAS par DS")
    add_total = False
    is_percentage = True
    rendering_type = 'graph'
    graph_type = 'column'
    graph_stacking = True

    INDICATORS = [
        SAMDeceasedRate,
        SAMHealedRate,
        SAMAbandonRate,
    ]


class SAMCaseloadTreatedByDS(SummaryForEntitiesTable):
    name = "MAS"
    caption = ("% caseload MAS traité par DS")
    rendering_type = 'graph'
    graph_type = 'column'
    is_percentage = True

    INDICATORS = [
        SAMCaseloadTreatedRate
    ]
