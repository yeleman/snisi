#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim: ai ts=4 sts=4 et sw=4 nu

from __future__ import (unicode_literals, absolute_import,
                        division, print_function)

from snisi_malaria.indicators.common import gen_shortcut
from snisi_malaria.indicators.section4 import TITLE as TITLE_4
from snisi_malaria.indicators.section4 import DecesToutesTranchesAge
from snisi_core.indicators import IndicatorTable, is_ref, ref_is, hide


class DecesToutAgeConfondu(IndicatorTable):
    """Tableau: Décès"""

    name = "Tableau 12"
    title = "Tout âge confond"
    caption = "Décès"
    rendering_type = 'table'
    add_percentage = True
    add_total = True

    INDICATORS = [
        is_ref(gen_shortcut('total_death_all_causes',
                            "Total des décès toutes causes confondues")),
        ref_is(0)(gen_shortcut('total_malaria_death',
                               "Total des décès pour paludisme")),
    ]


class ProportionDecesToutAgeConfondu(IndicatorTable):
    """ Graphe: Proportion de décès dû au  paludisme (par rapport aux

        décès toutes causes confondues) """
    name = "Figure 24"
    caption = ("Proportion de décès dû au  paludisme (par rapport aux "
               "décès toutes causes confondues) ")
    rendering_type = 'graph'
    as_percentage = True

    INDICATORS = [
        hide(is_ref(gen_shortcut('total_death_all_causes',
                                 "Total des décès toutes causes confondues"))),
        ref_is(0)(gen_shortcut('total_malaria_death',
                               "Pourcentage de décès dû au paludisme")),
    ]


WIDGETS = [DecesToutAgeConfondu,
           ProportionDecesToutAgeConfondu,
           DecesToutesTranchesAge]
TITLE = "{} / Tout âge confondu".format(TITLE_4)
