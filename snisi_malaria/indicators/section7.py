#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim: ai ts=4 sts=4 et sw=4 nu

from __future__ import (unicode_literals, absolute_import,
                        division, print_function)

from snisi_malaria.models import MalariaR
from snisi_malaria.indicators.common import MalariaIndicator
from snisi_malaria.indicators.map import NumberOfHealthUnitsReporting
from snisi_core.indicators import IndicatorTable, ref_is, is_ref, hide


class HealthUnitsWithoutArthemeterStockout(MalariaIndicator):
    name = "Structures sans rupture de stock d’Artheméter Injectable"

    def _compute(self):
        if self.is_hc():
            return self.report.stockout_artemether == self.report.NO

        nb_stockout = sum([bool(v == MalariaR.NO)
                           for v in self.all_hc_values('stockout_artemether')])
        return nb_stockout


class HealthUnitsWithoutQuinineStockout(MalariaIndicator):
    name = "Structures sans rupture de stock de Quinine"

    def _compute(self):
        if self.is_hc():
            return self.report.stockout_quinine == self.report.NO

        nb_stockout = sum([bool(v == MalariaR.NO)
                           for v in self.all_hc_values('stockout_quinine')])
        return nb_stockout


class HealthUnitsWithoutSerumStockout(MalariaIndicator):
    name = "Structures sans rupture de stock d’Artheméter Injectable"

    def _compute(self):
        if self.is_hc():
            return self.report.stockout_serum == self.report.NO

        nb_stockout = sum([bool(v == MalariaR.NO)
                           for v in self.all_hc_values('stockout_serum')])
        return nb_stockout


class PourcentageStructuresRuptureStockProduitPaluGrave(IndicatorTable):
    """ Tableau: Pourcentage de structures avec Rupture de stock en produits

    de prise en charge des cas de paludisme grave """

    name = "Tableau 18"
    title = " "
    caption = ("Pourcentage de structures avec rupture de stock en "
               "produits de prise en charge des cas de paludisme grave")
    rendering_type = 'table'
    add_percentage = True

    INDICATORS = [
        is_ref(NumberOfHealthUnitsReporting),
        ref_is(0)(HealthUnitsWithoutArthemeterStockout),
        ref_is(0)(HealthUnitsWithoutQuinineStockout),
        ref_is(0)(HealthUnitsWithoutSerumStockout)
    ]


class EvolutionStructuresRuptureStockProduitPaluGrave(IndicatorTable):
    """ Gaphe: Évolution des proportions  de cas de paludisme simple

        traités par CTA Chez les moins de 5 ans et les 5 ans et plus """

    name = "Figure 28"
    title = " "
    caption = "Evolution du pourcentage de structures sans rupture de stock" \
              " en produits de prise en charge des cas de paludisme grave"
    rendering_type = 'graph'
    graph_type = 'spline'
    as_percentage = True

    INDICATORS = [
        hide(is_ref(NumberOfHealthUnitsReporting)),
        ref_is(0)(HealthUnitsWithoutArthemeterStockout),
        ref_is(0)(HealthUnitsWithoutQuinineStockout),
        ref_is(0)(HealthUnitsWithoutSerumStockout)
    ]

WIDGETS = [PourcentageStructuresRuptureStockProduitPaluGrave,
           EvolutionStructuresRuptureStockProduitPaluGrave]

TITLE = "Gestion de stock de produits de PEC du paludisme grave"
