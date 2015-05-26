#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim: ai ts=4 sts=4 et sw=4 nu

from __future__ import (unicode_literals, absolute_import,
                        division, print_function)

from snisi_malaria.indicators.common import gen_shortcut
from snisi_malaria.indicators.section2a import TITLE as TITLE_2A
from snisi_core.indicators import IndicatorTable, is_ref, ref_is, hide


class CasPaludismeEnfantsMoins5ans(IndicatorTable):
    """ Tableau: Nombre de cas de paludisme chez les enfants de moins de

        5 ans """

    name = "Tableau 4"
    title = "Enfants moins de 5 ans"
    caption = "Nombre de cas de paludisme chez les enfants de moins de 5 ans"
    rendering_type = 'table'

    add_percentage = True
    add_total = True

    INDICATORS = [
        is_ref(gen_shortcut('u5_total_suspected_malaria_cases',
                            "Nombre de cas de paludisme (tous suspectés)")),
        ref_is(0)(gen_shortcut(
            'u5_total_tested_malaria_cases',
            "Total des cas suspects testés (GE et/ou TDR)")),
        ref_is(1)(gen_shortcut(
            'u5_total_confirmed_malaria_cases',
            "Nombre de cas suspects testés qui sont confirmés par GE ou TDR")),
        ref_is(2)(gen_shortcut('u5_total_simple_malaria_cases',
                               ". Cas simples")),
        ref_is(2)(gen_shortcut('u5_total_severe_malaria_cases',
                               ". Cas graves")),
    ]


class NbreTestesConfirmesUnderFive(IndicatorTable):
    """ Nombre de cas de paludisme  par mois (cas suspects, cas testés,

        cas confirmés)  chez les moins de 5 ans. """

    name = "Figure 6"
    caption = ("Nombre de cas de paludisme  par mois (cas suspects, "
               "cas testés,  cas confirmés)  chez les moins de 5 ans.")
    rendering_type = 'graph'
    graph_type = 'column'

    INDICATORS = [
        is_ref(gen_shortcut('u5_total_suspected_malaria_cases',
                            "Cas suspects")),
        ref_is(0)(gen_shortcut('u5_total_tested_malaria_cases', "Cas testés")),
        ref_is(0)(gen_shortcut('u5_total_confirmed_malaria_cases',
                               "Cas confirmés")),
    ]


class NbreTestesUnderFive(IndicatorTable):
    """ Evolution de la proportion des cas testés parmi les cas suspects

        chez les moins de 5 ans """

    name = "Figure 7"
    caption = ("Evolution de la proportion des cas testés parmi les cas "
               "suspects chez les moins de 5 ans")
    graph_type = 'spline'
    rendering_type = "graph"
    as_percentage = True

    INDICATORS = [
        hide(is_ref(gen_shortcut('u5_total_suspected_malaria_cases',
                                 "Cas suspects"))),
        ref_is(0)(gen_shortcut('u5_total_tested_malaria_cases',
                               "% Cas testés")),
    ]


class NbreConfirmesUnderFive(IndicatorTable):
    """ Evolution de la proportion des cas confirmés parmi les cas testés

        chez les moins de 5 ans """

    name = "Figure 8"
    caption = ("Evolution de la proportion des cas confirmés parmi les "
               "cas testés  chez les moins de 5 ans")
    graph_type = 'spline'
    rendering_type = 'graph'
    as_percentage = True

    INDICATORS = [
        hide(is_ref(gen_shortcut('u5_total_tested_malaria_cases',
                                 "Cas suspects"))),
        ref_is(0)(gen_shortcut('u5_total_confirmed_malaria_cases',
                               "% Cas confirmés")),
    ]


class NbreCasSimplesGravesUnderFive(IndicatorTable):
    """ Evolution de la proportion des cas confirmés parmi les cas testés

        chez les moins de 5 ans """

    name = "Figure 9"
    caption = ("Proportion de cas simples et cas graves chez les moins "
               "de 5 ans ")
    graph_type = 'spline'
    rendering_type = 'graph'
    as_percentage = True

    INDICATORS = [
        hide(gen_shortcut('u5_total_confirmed_malaria_cases',
                          "Cas confirmés")),
        ref_is(0)(gen_shortcut('u5_total_simple_malaria_cases',
                               "% Cas simples")),
        ref_is(0)(gen_shortcut('u5_total_severe_malaria_cases', "% Cas graves")),
    ]


WIDGETS = [CasPaludismeEnfantsMoins5ans,
           NbreTestesConfirmesUnderFive,
           NbreTestesUnderFive,
           NbreConfirmesUnderFive,
           NbreCasSimplesGravesUnderFive]
TITLE = "{} / Moins de 5 ans".format(TITLE_2A)
