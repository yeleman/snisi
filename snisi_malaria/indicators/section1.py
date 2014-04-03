#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim: ai ts=4 sts=4 et sw=4 nu

from __future__ import (unicode_literals, absolute_import,
                        division, print_function)

from snisi_malaria.models import MalariaR
from snisi_malaria.indicators.common import MalariaIndicator
from snisi_core.indicators import IndicatorTable
from snisi_malaria.indicators.common import gen_shortcut
from snisi_core.indicators import IndicatorTable, is_ref, ref_is, hide


class TableauPromptitudeRapportage(IndicatorTable):

    name = "Tableau 1"
    title = ""
    caption = ("Pourcentage de structures ayant transmis leurs formulaires "
               "de collecte dans les délais prévus")
    rendering_type = 'table'

    INDICATORS = [
        is_ref(gen_shortcut('nb_source_reports_expected',
                            "Nombre de rapports attendus")),
        ref_is(0)(gen_shortcut('nb_source_reports_arrived',
                               "Nombre de rapports reçus")),
        ref_is(0)(gen_shortcut('nb_source_reports_arrived_on_time',
                               "Nombre de rapports reçus à temps")),
    ]


class FigurePromptitudeRapportage(IndicatorTable):

    name = "Figure 1"
    title = ""
    caption = ("Évolution de la promptitude de la notification")
    rendering_type = 'graph'
    graph_type = 'spline'
    as_percentage = True

    INDICATORS = [
        hide(is_ref(gen_shortcut('nb_source_reports_expected',
                            "Nombre de rapports attendus"))),
        ref_is(0)(gen_shortcut('nb_source_reports_arrived',
                               "Nombre de rapports reçus")),
        ref_is(0)(gen_shortcut('nb_source_reports_arrived_on_time',
                               "Nombre de rapports reçus à temps")),
    ]


WIDGETS = [
    TableauPromptitudeRapportage,
    FigurePromptitudeRapportage
]
TITLE = "Identification de la structure ayant notifié les données"
