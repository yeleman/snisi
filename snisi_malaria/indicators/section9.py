#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim: ai ts=4 sts=4 et sw=4 nu

from __future__ import (unicode_literals, absolute_import,
                        division, print_function)


from snisi_malaria.indicators.common import gen_shortcut
from snisi_core.indicators import IndicatorTable


class DonneesCPNetTPI(IndicatorTable):
    """ Tableau: Données sur la CPN et le Traitement Préventif  Intermittent

        (TPI) """

    name = "Tableau 20"
    title = " "
    caption = ("Données sur la CPN et le Traitement Préventif "
               "Intermittent(TPI)")
    rendering_type = 'table'

    INDICATORS = [
        gen_shortcut('pw_total_anc1',
                     "Nombre de femmes enceintes reçues en CPN  1"),
        gen_shortcut('pw_total_sp1',
                     "Nombre de femmes enceintes ayant reçu la SP1"),
        gen_shortcut('pw_total_sp2',
                     "Nombre de femmes enceintes ayant reçu la SP2"),
    ]


class EvolutionCPN1SP1SP2(IndicatorTable):
    """ Graphe: Evolution de la  CPN1, SP1 et SP2 chez les femmes enceintes"""

    name = "Figure 30"
    title = " "
    caption = "Evolution du nombre de SP1 et SP2 chez les femmes enceintes"
    rendering_type = 'graph'
    graph_type = 'spline'

    INDICATORS = [
        gen_shortcut('pw_total_sp1',
                     "Nombre de femmes enceintes ayant reçu la SP1"),
        gen_shortcut('pw_total_sp2',
                     "Nombre de femmes enceintes ayant reçu la SP2"),
    ]


class NombreFemmesEnceintesCPN1NombreMILDFemmesEnceintes(IndicatorTable):
    """ Graphe: Nombre de femmes enceintes reçues en CPN1 et Nombre de

        MILD distribuées aux femmes enceintes"""

    name = "Figure 31"
    title = " "
    caption = ("Nombre de femmes enceintes reçues en CPN1 et Nombre "
               "de MILD distribuées aux femmes enceintes")
    rendering_type = 'graph'

    INDICATORS = [
        gen_shortcut('pw_total_anc1',
                     "Nombre de femmes enceintes reçues en CPN  1"),
        gen_shortcut('pw_total_distributed_bednets',
                     "Nbre MILD distribuees aux femmes enceintes"),
    ]

WIDGETS = [DonneesCPNetTPI,
           EvolutionCPN1SP1SP2,
           NombreFemmesEnceintesCPN1NombreMILDFemmesEnceintes]
TITLE = "CPN et Traitement Préventif Intermittent (TPI)"
