#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim: ai ts=4 sts=4 et sw=4 nu

from __future__ import (unicode_literals, absolute_import,
                        division, print_function)

from snisi_malaria.indicators.common import gen_shortcut
from snisi_core.indicators import IndicatorTable, is_ref, ref_is, hide


class DecesToutesTranchesAge(IndicatorTable):
    """ Graphe: Evolution du nombre de décès dû au paludisme Chez les

        moins de 5 ans, les 5 ans et plus et les femmes enceintes """

    name = "Figure 25"
    title = ""
    caption = "Evolution du nombre de décès dû au paludisme Chez les moins " \
              "de 5 ans, les 5 ans et plus et les femmes enceintes"
    rendering_type = 'graph'
    graph_type = 'spline'

    INDICATORS = [
        hide(is_ref(gen_shortcut('total_death_all_causes',
                                 "Total des décès toutes causes confondues"))),
        ref_is(0)(gen_shortcut('o5_total_malaria_death',
                               "Personnes de 5 ans et plus")),
        ref_is(0)(gen_shortcut('u5_total_malaria_death',
                               "Enfants de moins de 5 ans")),
        ref_is(0)(gen_shortcut('pw_total_malaria_death',
                               "Femmes enceintes")),
    ]

TITLE = "Décès"
