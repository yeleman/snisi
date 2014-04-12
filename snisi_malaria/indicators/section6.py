#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim: ai ts=4 sts=4 et sw=4 nu

from __future__ import (unicode_literals, absolute_import,
                        division, print_function)

from snisi_malaria.models import MalariaR
from snisi_malaria.indicators.common import MalariaIndicator
from snisi_malaria.indicators.map import NumberOfHealthUnitsReporting
from snisi_core.indicators import IndicatorTable, ref_is, is_ref, hide


class HealthUnitsWithoutACTYouthStockout(MalariaIndicator):
    name = "Structures sans rupture de stock en CTA Adolescent"

    def _compute(self):
        if self.is_hc():
            return self.report.stockout_act_youth == self.report.NO

        nb_stockout = sum([bool(v == MalariaR.NO) for v in self.all_hc_values('stockout_act_youth')])
        return nb_stockout


class HealthUnitsWithoutACTAdultStockout(MalariaIndicator):
    name = "Structures sans rupture de stock en CTA Adulte"

    def _compute(self):
        if self.is_hc():
            return not self.report.stockout_act_adult == self.report.NO

        nb_stockout = sum([bool(v == MalariaR.NO) for v in self.all_hc_values('stockout_act_adult')])
        return nb_stockout


class HealthUnitsWithoutACTChildrenStockout(MalariaIndicator):
    name = "Structures sans rupture de stock en CTA Nourisson-Enfant"

    def _compute(self):
        if self.is_hc():
            return not self.report.stockout_act_children == self.report.NO

        nb_stockout = sum([bool(v == MalariaR.NO) for v in self.all_hc_values('stockout_act_children')])
        return nb_stockout


class PourcentageStructuresRuptureStockCTADistrict(IndicatorTable):
    """ Tableau: Pourcentage de structures sans Rupture de stock de CTA s"""

    name = "Tableau 17"
    title = " "
    caption = ("Pourcentage de structures sans Rupture de stock de CTA dans "
               "le district")
    rendering_type = 'table'
    add_percentage = True

    INDICATORS = [
        is_ref(NumberOfHealthUnitsReporting),
        ref_is(0)(HealthUnitsWithoutACTChildrenStockout),
        ref_is(0)(HealthUnitsWithoutACTYouthStockout),
        ref_is(0)(HealthUnitsWithoutACTAdultStockout)
    ]


class EvolutionPourcentageStructuresRuptureStockCTA(IndicatorTable):
    """ Graphe: Evolution du pourcentage de Structures sans rupture de stock en

        CTA """

    name = "Figure 27"
    title = " "
    caption = ("Evolution du pourcentage de Structures sans rupture de "
               "stock en CTA (Nourrisson-Enfant, Adolescent, Adulte")
    rendering_type = 'graph'
    graph_type = 'spline'
    with_percentage = True

    INDICATORS = [
        hide(is_ref(NumberOfHealthUnitsReporting)),
        ref_is(0)(HealthUnitsWithoutACTChildrenStockout),
        ref_is(0)(HealthUnitsWithoutACTYouthStockout),
        ref_is(0)(HealthUnitsWithoutACTAdultStockout)
    ]

WIDGETS = [PourcentageStructuresRuptureStockCTADistrict,
           EvolutionPourcentageStructuresRuptureStockCTA]
TITLE = "Gestion de stock de CTA"
