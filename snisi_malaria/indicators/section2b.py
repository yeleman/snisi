#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim: ai ts=4 sts=4 et sw=4 nu

from __future__ import (unicode_literals, absolute_import,
                        division, print_function)

from snisi_malaria.indicators.common import gen_shortcut
from snisi_core.indicators import IndicatorTable, is_ref, ref_is


class CasPaludismeSimpleTraitesCTA(IndicatorTable):
    """ Tableau: Cas de paludisme simple traités par CTA """

    name = "Tableau 7"
    title = " "
    caption = "Cas de paludisme simple traités par CTA"
    add_percentage = True
    add_total = True

    INDICATORS = [
        is_ref(gen_shortcut('u5_total_simple_malaria_cases',
                            "Nbre de cas simple moins de 5ans")),
        ref_is(0)(gen_shortcut('u5_total_treated_malaria_cases',
                               "Nbre de cas traités par CTA moins de 5ans")),
        is_ref(gen_shortcut('o5_total_simple_malaria_cases',
                            "Nbre de cas simple 5ans et plus")),
        ref_is(2)(gen_shortcut('o5_total_treated_malaria_cases',
                               "Nbre de cas traités par CTA 5ans et plus")),
        gen_shortcut('total_confirmed_malaria_cases', "Nbre de cas confirmés"),
        is_ref(gen_shortcut('total_simple_malaria_cases',
                            "Nbre de cas simple")),
        ref_is(2)(gen_shortcut('total_treated_malaria_cases',
                               "Nbre de cas traités par CTA")),
    ]


class CasPaludismeConfirmesTraitesCTA(IndicatorTable):
    """ Graphe: Nombre de cas de paludisme confirmés et nombre de cas traités

        par CTA """

    name = "Figure 17"
    title = " "
    caption = ("Nombre de cas de paludisme confirmés et "
               "nombre de cas traités par CTA")
    rendering_type = 'graph'
    graph_type = 'column'

    INDICATORS = [
        gen_shortcut('total_confirmed_malaria_cases',
                     "Nbre de cas confirmés"),
        gen_shortcut('total_treated_malaria_cases',
                     "Nbre de cas traités par CTA"),
    ]


class EvolutionProportionCasPaludismeSimpleTraitesU5O5(IndicatorTable):
    """ Graphe: Évolution des proportions  de cas de paludisme simple

        traités par CTA Chez les moins de 5 ans et les 5 ans et plus """

    name = "Figure 18"
    title = " "
    caption = ("Évolution des cas de paludisme "
               "simple traités par CTA Chez les moins de 5 ans "
               "et les 5 ans et plus")
    rendering_type = 'graph'
    graph_type = 'column'

    INDICATORS = [
        gen_shortcut('u5_total_treated_malaria_cases',
                     "Nbre de cas traités par CTA chez les moins de 5 ans"),
        gen_shortcut('o5_total_treated_malaria_cases',
                     "Nbre de cas traités par CTA chez les 5 ans et plus")
    ]


class EvolutionProportionCasPaludismeSimpleTraitesu5O51(IndicatorTable):
    """ Graphe: Évolution des proportions  de cas de paludisme simple

        traités par CTA Chez les moins de 5 ans et les 5 ans et plus """

    name = "Figure 19"
    title = " "
    caption = ("Évolution des cas de paludisme "
               "simple traités par CTA Chez les moins de 5 ans "
               "et les 5 ans et plus")
    rendering_type = 'graph'
    graph_type = 'spline'

    INDICATORS = [
        gen_shortcut('u5_total_treated_malaria_cases',
                     "Nbre de cas traités par CTA chez les moins de 5 ans"),
        gen_shortcut('o5_total_treated_malaria_cases',
                     "Nbre de cas traités par CTA chez les 5 ans et plus")
    ]

WIDGETS = [CasPaludismeSimpleTraitesCTA,
           CasPaludismeConfirmesTraitesCTA,
           EvolutionProportionCasPaludismeSimpleTraitesU5O5,
           EvolutionProportionCasPaludismeSimpleTraitesu5O51]
TITLE = "Traitement par CTA"
