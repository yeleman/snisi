#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim: ai ts=4 sts=4 et sw=4 nu

from __future__ import (unicode_literals, absolute_import,
                        division, print_function)

from snisi_malaria.indicators.common import gen_shortcut
from snisi_malaria.indicators.section4 import TITLE as TITLE_4
from snisi_malaria.indicators.section4 import DecesToutesTranchesAge
from snisi_core.indicators import IndicatorTable, is_ref, ref_is


class DecesOverFive(IndicatorTable):
    """ Tableau: Décès notifiés chez les 5 ans et plus """

    name = "Tableau 14"
    title = "5 ans et plus"
    caption = "Décès notifiés pour le trimestre chez les 5 ans et plus"
    rendering_type = 'table'
    add_percentage = True
    add_total = True

    INDICATORS = [
        is_ref(gen_shortcut('o5_total_death_all_causes',
                            "Total des décès toutes causes confondues")),
        ref_is(0)(gen_shortcut('o5_total_malaria_death',
                               "Total des décès pour paludisme")),
    ]


WIDGETS = [DecesOverFive,
           DecesToutesTranchesAge]
TITLE = "{} / 5 ans et plus".format(TITLE_4)
