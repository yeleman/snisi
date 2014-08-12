#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim: ai ts=4 sts=4 et sw=4 nu

from __future__ import (unicode_literals, absolute_import,
                        division, print_function)

from snisi_malaria.models import MalariaR
from snisi_malaria.indicators.common import MalariaIndicator, gen_shortcut
from snisi_malaria.indicators.map import NumberOfHealthUnitsReporting
from snisi_core.indicators import IndicatorTable, ref_is, is_ref, hide


class CTAMILD(IndicatorTable):
    """ Tableau: Données sur la CPN et le Traitement Préventif  Intermittent

        (TPI) """

    name = "Tableau 27"
    title = " "
    caption = ("Pourcentage de femmes enceintes vues en CPN ayant reçu une "
               "MILD ou un SP2")
    rendering_type = 'table'

    INDICATORS = [
        is_ref(gen_shortcut('pw_total_anc1',
                            "femmes enceintes reçues en CPN")),
        ref_is(0)(gen_shortcut('pw_total_distributed_bednets',
                               "MILD distribuées aux femmes enceintes")),
        ref_is(0)(gen_shortcut('pw_total_sp2',
                               "femmes enceintes ayant reçu la SP2"))
    ]


class GrapheCTAMILD(CTAMILD):
    """ Graphe: Evolution de la  CPN1, SP1 et SP2 chez les femmes enceintes"""

    name = "Figure 37"
    title = " "
    caption = ("Pourcentage de femmes enceintes vues en CPN ayant reçu une "
               "MILD ou un SP2")
    graph_type = 'spline'
    rendering_type = 'graph'
    as_percentage = True

    INDICATORS = [
        hide(is_ref(gen_shortcut('pw_total_anc1',
                                 "femmes enceintes reçues en CPN"))),
        ref_is(0)(gen_shortcut('pw_total_distributed_bednets',
                               "% MILD distribuées aux femmes enceintes")),
        ref_is(0)(gen_shortcut('pw_total_sp2',
                               "% femmes enceintes ayant reçu la SP2"))
    ]


class TraitesCTA(IndicatorTable):
    """ Tableau: Données sur la CPN et le Traitement Préventif  Intermittent

        (TPI) """

    name = "Tableau 28"
    title = " "
    caption = "Pourcentage de cas traités par CTA"
    rendering_type = 'table'


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


class HealthUnitsWithoutACTStockout(MalariaIndicator):
    name = "Structures sans rupture de stock de CTA"

    def _compute(self):
        if self.is_hc():
            return (self.report.stockout_act_children == self.report.NO
                    or self.report.stockout_act_youth == self.report.NO
                    or self.report.stockout_act_adult == self.report.NO)

        nb_stockout = 0
        for r in self.report.indiv_sources.all():
            if (getattr(r, 'stockout_act_children') == MalariaR.NO
                    or getattr(r, 'stockout_act_youth') == MalariaR.NO
                    or getattr(r, 'stockout_act_adult') == MalariaR.NO):
                nb_stockout += 1
        return nb_stockout


class PourcentageCTATDRMILD(IndicatorTable):
    """ Tableau: Pourcentage de structures sans Rupture de stock de CTA dans

        le district """

    name = "Tableau 29"
    title = " "
    caption = ("Pourcentage de structures sans Rupture de stock de CTA, "
               "TDR et MILD")
    redering_type = 'table'
    add_percentage = True

    INDICATORS = [
        is_ref(NumberOfHealthUnitsReporting),
        ref_is(0)(HealthUnitsWithoutACTStockout),
        ref_is(0)(HealthUnitsWithoutRDTStockout),
        ref_is(0)(HealthUnitsWithoutBednetStockout)
    ]


class GraphePourcentageCTATDRMILD(IndicatorTable):
    """ Graphe: Nombre de femmes enceintes reçues en CPN1 et Nombre de

        MILD distribuées aux femmes enceintes"""

    name = "Figure 39"
    title = " "
    caption = ("Pourcentage de structures sans Rupture de stock "
               " de CTA, TDR et MILD")
    graph_type = 'spline'
    rendering_type = 'graph'
    as_percentage = True

    INDICATORS = [
        hide(is_ref(NumberOfHealthUnitsReporting)),
        ref_is(0)(HealthUnitsWithoutACTStockout),
        ref_is(0)(HealthUnitsWithoutRDTStockout),
        ref_is(0)(HealthUnitsWithoutBednetStockout)
    ]

WIDGETS = [CTAMILD, GrapheCTAMILD,
           # TraitesCTA, GrapheTraitesCTA,
           PourcentageCTATDRMILD, GraphePourcentageCTATDRMILD]
TITLE = "Données sur les intrants"
