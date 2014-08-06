#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim: ai ts=4 sts=4 et sw=4 nu

from __future__ import (unicode_literals, absolute_import,
                        division, print_function)

from snisi_malaria.indicators.common import gen_shortcut
from snisi_malaria.indicators.section2a import TITLE as TITLE_2A
from snisi_core.indicators import IndicatorTable, is_ref, ref_is, hide


class CasPaludismeEnfantsPlusDe5ans(IndicatorTable):
    """ Tableau: Nombre de cas de paludisme chez les personnes de 5 ans et

        plus """

    name = "Tableau 5"
    title = "Personnes de 5 ans et plus"
    caption = "Nombre de cas de paludisme chez les personnes de 5 ans et plus"
    rendering_type = 'table'

    add_percentage = True
    add_total = True

    INDICATORS = [
        is_ref(gen_shortcut('o5_total_suspected_malaria_cases',
                            "Nombre de cas de paludisme (tous suspectés)")),
        ref_is(0)(gen_shortcut(
            'o5_total_tested_malaria_cases',
            "Total des cas suspects testés (GE et/ou TDR)")),
        ref_is(1)(gen_shortcut(
            'o5_total_confirmed_malaria_cases',
            "Nombre de cas suspects testés qui sont confirmés par GE ou TDR")),
        ref_is(2)(gen_shortcut('o5_total_simple_malaria_cases',
                               ". Cas simples")),
        ref_is(2)(gen_shortcut('o5_total_severe_malaria_cases',
                               ". Cas graves")),

    ]


class NbreTestesConfirmesOverFive(IndicatorTable):
    """ Graphe: Evolution de la proportion des cas testés parmi les cas

       et proportion des cas confirmés parmi les cas testés  chez
       les de 5 ans et plus """

    name = "Figure 10"
    caption = ("Nombre de cas de paludisme  par mois (cas suspects, "
               "cas testés,  cas confirmés)  chez les personnes de "
               "5 ans et plus.")
    rendering_type = 'graph'
    graph_type = 'column'

    INDICATORS = [
        is_ref(gen_shortcut('o5_total_suspected_malaria_cases',
                            "Cas suspects")),
        ref_is(0)(gen_shortcut('o5_total_tested_malaria_cases', "Cas testés")),
        ref_is(0)(gen_shortcut('o5_total_confirmed_malaria_cases',
                               "Cas confirmés")),
    ]


class NbreTestesOverFive(IndicatorTable):
    """ Graphe: Evolution de la proportion des cas testés parmi les cas

       et proportion des cas confirmés parmi les cas testés  chez les
       de 5 ans et plus """

    name = "Figure 11"
    caption = ("Evolution de la proportion des cas testés parmi les "
               "cas suspects chez les personnes de 5 ans et plus")
    graph_type = 'spline'
    rendering_type = "graph"
    as_percentage = True

    INDICATORS = [
        hide(is_ref(gen_shortcut('o5_total_suspected_malaria_cases',
                                 "Cas suspects"))),
        ref_is(0)(gen_shortcut('o5_total_tested_malaria_cases',
                               "Cas testés")),
    ]


class NbreConfirmesOverFive(IndicatorTable):
    """ Graphe: Evolution de la proportion des cas confirmés parmi

        les cas testés  chez les personnes de 5 ans et plus """

    name = "Figure 12"
    caption = ("Evolution de la proportion des cas confirmés parmi"
               "les cas testés  chez les personnes de 5 ans et plus")
    graph_type = 'spline'
    rendering_type = 'graph'
    as_percentage = True

    INDICATORS = [
        hide(is_ref(gen_shortcut('o5_total_suspected_malaria_cases',
                                 "Cas suspects"))),
        ref_is(0)(gen_shortcut('o5_total_confirmed_malaria_cases',
                               "Cas confirmés")),
    ]


class NbreCasSimplesGravesOverFive(IndicatorTable):
    """ Graphe: Evolution de la proportion des cas testés parmi les cas

       et proportion des cas confirmés parmi les cas testés  chez les
       de 5 ans et plus """

    name = "Figure 13"
    caption = ("Evolution de la proportion des cas testés parmi "
               "les cas suspects et proportion des cas confirmés "
               "parmi les cas testés  chez les personnes de 5 ans "
               "et plus")
    graph_type = 'spline'
    rendering_type = 'graph'
    as_percentage = True

    INDICATORS = [
        hide(gen_shortcut('o5_total_confirmed_malaria_cases',
                          "Cas confirmés")),
        ref_is(0)(gen_shortcut('o5_total_simple_malaria_cases',
                               "Cas simples")),
        ref_is(0)(gen_shortcut('o5_total_severe_malaria_cases',
                               "Cas graves")),
    ]


WIDGETS = [CasPaludismeEnfantsPlusDe5ans,
           NbreTestesConfirmesOverFive,
           NbreTestesOverFive,
           NbreConfirmesOverFive,
           NbreCasSimplesGravesOverFive]
TITLE = "{} / 5 ans et plus".format(TITLE_2A)
