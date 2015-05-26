#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim: ai ts=4 sts=4 et sw=4 nu

from __future__ import (unicode_literals, absolute_import,
                        division, print_function)

from snisi_malaria.indicators.common import gen_shortcut
from snisi_malaria.indicators.section2a import TITLE as TITLE_2A
from snisi_core.indicators import IndicatorTable, is_ref, ref_is, hide


class CasPaludismeFemmesEnceintes(IndicatorTable):
    """ Tableau: Nombre de cas de paludisme chez les femmes enceintes """

    name = "Tableau 6"
    title = "Femmes enceintes"
    caption = "Nombre de cas de paludisme chez les femmes enceintes"
    rendering_type = 'table'

    add_percentage = True
    add_total = True

    INDICATORS = [
        is_ref(gen_shortcut('pw_total_suspected_malaria_cases',
                            "Nombre de cas de paludisme (tous suspectés)")),
        ref_is(0)(gen_shortcut(
            'pw_total_tested_malaria_cases',
            "Total des cas suspects testés (GE et/ou TDR)")),
        ref_is(2)(gen_shortcut(
            'pw_total_confirmed_malaria_cases',
            "Nombre de cas suspects testés qui sont confirmés "
            "par GE ou TDR(cas graves)")),
    ]


class NbreTestesConfirmesPregnantWomen(IndicatorTable):
    """ Nombre de cas de paludisme  par mois (cas suspects,

        cas testés,  cas confirmés)  chez les femmes enceintes. """

    name = "Figure 14"
    caption = ("Nombre de cas de paludisme  par mois (cas suspects, "
               "cas testés,  cas confirmés)  chez les femmes enceintes.")
    rendering_type = 'graph'
    graph_type = 'column'

    INDICATORS = [
        is_ref(gen_shortcut('pw_total_suspected_malaria_cases',
                            "Cas suspects")),
        ref_is(0)(gen_shortcut('pw_total_tested_malaria_cases', "Cas testés")),
        ref_is(0)(gen_shortcut('pw_total_confirmed_malaria_cases',
                               "Cas confirmés")),
    ]


class NbreTestesPregnantWomen(IndicatorTable):
    """ Graphe: Evolution de la proportion des cas testés parmi les

        cas suspects chez les femmes enceintes. """

    name = "Figure 15"
    caption = ("Evolution de la proportion des cas testés parmi les "
               "cas suspects chez les femmes enceintes. ")
    graph_type = 'spline'
    rendering_type = "graph"
    as_percentage = True

    INDICATORS = [
        hide(is_ref(gen_shortcut('pw_total_suspected_malaria_cases',
                                 "Cas suspects"))),
        ref_is(0)(gen_shortcut('pw_total_tested_malaria_cases',
                               "% Cas testés")),
    ]


class NbreConfirmesPregnantWomen(IndicatorTable):
    """ Graphe: Evolution de la proportion des cas confirmés parmi

        les cas testés  chez les femmes enceintes. """

    name = "Figure 16"
    caption = ("Evolution de la proportion des cas confirmés parmi "
               " les cas testés  chez les femmes enceintes")
    graph_type = 'spline'
    rendering_type = 'graph'
    as_percentage = True

    INDICATORS = [
        hide(is_ref(gen_shortcut('pw_total_tested_malaria_cases',
                                 "Cas suspects"))),
        ref_is(0)(gen_shortcut('pw_total_confirmed_malaria_cases',
                               "% Cas confirmés")),
    ]


WIDGETS = [CasPaludismeFemmesEnceintes,
           NbreTestesConfirmesPregnantWomen,
           NbreTestesPregnantWomen,
           NbreConfirmesPregnantWomen]
TITLE = "{} / Femmes enceintes".format(TITLE_2A)
