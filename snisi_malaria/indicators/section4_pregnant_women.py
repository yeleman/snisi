#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim: ai ts=4 sts=4 et sw=4 nu

from __future__ import (unicode_literals, absolute_import,
                        division, print_function)

from snisi_malaria.indicators.common import gen_shortcut
from snisi_malaria.indicators.section4 import TITLE as TITLE_4
from snisi_malaria.indicators.section4 import DecesToutesTranchesAge
from snisi_core.indicators import IndicatorTable, is_ref, ref_is


class DecesPregnantWomen(IndicatorTable):
    """ Décès notifiés chez les femmes enceintes """

    name = "Tableau 15"
    title = "Femmes enceintes"
    caption = "Décès notifiés chez les femmes enceintes"
    rendering_type = 'table'
    add_percentage = True
    add_total = True

    INDICATORS = [
        is_ref(gen_shortcut('pw_total_death_all_causes',
                            "Total des décès toutes causes confondues")),
        ref_is(0)(gen_shortcut('pw_total_malaria_death',
                               "Total des décès pour paludisme")),
    ]


WIDGETS = [DecesPregnantWomen,
           DecesToutesTranchesAge]
TITLE = "{} / Femmes enceintes".format(TITLE_4)
