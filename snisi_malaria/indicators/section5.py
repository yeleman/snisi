#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim: ai ts=4 sts=4 et sw=4 nu

from __future__ import (unicode_literals, absolute_import,
                        division, print_function)

from snisi_malaria.indicators.common import gen_shortcut
from snisi_core.indicators import IndicatorTable


class NombreMoustiquqiresImpregneesInsecticidesLongueDureeMILD(IndicatorTable):
    """ Tableau: Nombre de Moustiquaires imprégnées  d’Insecticides

       de Longue Durée (MILD) distribuées"""

    name = "Tableau 16"
    title = " "
    caption = ("Nombre de Moustiquaires imprégnées  d’Insecticides de "
               "Longue Durée (MILD) distribuées")
    rendering_type = 'table'

    INDICATORS = [
        gen_shortcut('u5_total_distributed_bednets',
                     "Nombre MILD distribuées aux enfants de moins de 5 ans"),
        gen_shortcut('pw_total_distributed_bednets',
                     "Nombre de MILD distribuées aux femmes enceintes"),
    ]



class EvolutionNbreMILDMoins5ansFemmesenceintes(IndicatorTable):
    """Graphe: Evolution du nombre de MILD distribuées aux moins

       de 5 ans et femmes enceintes"""

    name = "Figure 26"
    title = " "
    caption = ("Evolution du nombre de MILD distribuées aux moins de "
               "5 ans et femmes enceintes")
    rendering_type = 'graph'
    graph_type = 'spline'

    INDICATORS = [
        gen_shortcut('u5_total_distributed_bednets',
                     "Nombre MILD distribuées aux enfants de moins de 5 ans"),
        gen_shortcut('pw_total_distributed_bednets',
                     "Nombre de MILD distribuées aux femmes enceintes"),
    ]

WIDGETS = [NombreMoustiquqiresImpregneesInsecticidesLongueDureeMILD,
           EvolutionNbreMILDMoins5ansFemmesenceintes]
TITLE = "Moustiquaires imprégnées d’Insecticides de Longue Durée (MILD)"
