#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim: ai ts=4 sts=4 et sw=4 nu

from __future__ import (unicode_literals, absolute_import,
                        division, print_function)

from snisi_malaria.models import MalariaR
from snisi_malaria.indicators.common import MalariaIndicator
from snisi_malaria.indicators.map import NumberOfHealthUnitsReporting
from snisi_core.indicators import IndicatorTable, ref_is, is_ref, hide


class HealthUnitsWithoutBednetStockout(MalariaIndicator):
    name = "Structures sans rupture de stock de MILD"

    def _compute(self):
        if self.is_hc():
            return self.report.stockout_bednet == self.report.NO

        nb_stockout = sum([bool(v == MalariaR.NO)
                           for v in self.all_hc_values('stockout_bednet')])
        return nb_stockout


class HealthUnitsWithoutRDTStockout(MalariaIndicator):
    name = "Structures sans rupture de stock de TDR"

    def _compute(self):
        if self.is_hc():
            return self.report.stockout_rdt == self.report.NO

        nb_stockout = sum([bool(v == MalariaR.NO)
                           for v in self.all_hc_values('stockout_rdt')])
        return nb_stockout


class HealthUnitsWithoutSPStockout(MalariaIndicator):
    name = "Structures sans rupture de stock de SP"

    def _compute(self):
        if self.is_hc():
            return self.report.stockout_sp == self.report.NO

        nb_stockout = sum([bool(v == MalariaR.NO)
                           for v in self.all_hc_values('stockout_sp')])
        return nb_stockout


class PourcentageStructuresRuptureStockMILDTDRSP(IndicatorTable):
    """ Tableau: Pourcentage de structures sans rupture

        de stock en MILD, TDR, SP """

    name = "Tableau 19"
    title = " "
    caption = ("Pourcentage de structures sans rupture de stock en "
               "MILD, TDR, SP")
    rendering_type = 'table'
    add_percentage = True

    INDICATORS = [
        is_ref(NumberOfHealthUnitsReporting),
        ref_is(0)(HealthUnitsWithoutBednetStockout),
        ref_is(0)(HealthUnitsWithoutRDTStockout),
        ref_is(0)(HealthUnitsWithoutSPStockout)
    ]


class EvolutionPourcentageStructuresRuptureStockMILDTDRSP(IndicatorTable):
    """ Graphe: Evolution du pourcentage de Structures

        sans rupture de stock en MILD, TDR, SP """

    name = "Figure 29"
    title = " "
    caption = ("Evolution du pourcentage de Structures sans rupture de "
               "stock en MILD, TDR, SP")
    rendering_type = 'graph'
    graph_type = 'spline'
    as_percentage = True

    INDICATORS = [
        hide(is_ref(NumberOfHealthUnitsReporting)),
        ref_is(0)(HealthUnitsWithoutBednetStockout),
        ref_is(0)(HealthUnitsWithoutRDTStockout),
        ref_is(0)(HealthUnitsWithoutSPStockout)
    ]

WIDGETS = [PourcentageStructuresRuptureStockMILDTDRSP,
           EvolutionPourcentageStructuresRuptureStockMILDTDRSP]
TITLE = "Gestion de stock MILD, TDR, SP"
